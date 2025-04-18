"""AI service integrations for Task Blaster."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import anthropic
from anthropic import AsyncAnthropic, AnthropicBedrock
from openai import OpenAI
from rich.progress import Progress

from .config import config
from .ui import create_loading_indicator
from .utils import log, sanitize_prompt

def get_anthropic_client() -> Optional[Union[AsyncAnthropic, AnthropicBedrock]]:
    """Get appropriate Anthropic client based on configuration."""
    try:
        if config.use_bedrock:
            # Initialize Bedrock client
            client_kwargs = {
                "aws_region": config.aws_region
            }
            
            # Add AWS credentials if provided
            if config.aws_access_key and config.aws_secret_key:
                client_kwargs.update({
                    "aws_access_key": config.aws_access_key,
                    "aws_secret_key": config.aws_secret_key
                })
                
                if config.aws_session_token:
                    client_kwargs["aws_session_token"] = config.aws_session_token
            
            return AnthropicBedrock(**client_kwargs)
            
        elif config.anthropic_api_key:
            # Initialize direct Anthropic client
            return AsyncAnthropic(api_key=config.anthropic_api_key)
        
        return None
        
    except Exception as e:
        log.warning(f"Failed to initialize Anthropic client: {e}")
        return None

def get_perplexity_client() -> Optional[OpenAI]:
    """Get Perplexity client if API key is available."""
    if not config.perplexity_api_key:
        return None
    try:
        return OpenAI(
            api_key=config.perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
    except Exception as e:
        log.warning(f"Failed to initialize Perplexity client: {e}")
        return None

# Initialize clients
anthropic_client = get_anthropic_client()
perplexity_client = get_perplexity_client()

async def call_claude(
    content: str,
    prd_path: Union[str, Path],
    num_tasks: int = 10
) -> Dict[str, Any]:
    """Call Claude to generate tasks from PRD content."""
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )

    system_prompt = f"""You are a technical lead helping to break down a PRD into specific tasks.
Given a PRD, generate {num_tasks} concrete, actionable tasks that would be needed to implement it.

For each task, include:
1. A clear, specific title
2. A detailed description
3. Implementation details
4. A test strategy
5. Dependencies on other tasks (by ID)
6. Priority (low, medium, high)

Return the tasks as a JSON object with this structure:
{{
    "tasks": [
        {{
            "id": 1,
            "title": "Task title",
            "description": "Task description",
            "details": "Implementation details",
            "testStrategy": "How to test this task",
            "dependencies": [],
            "priority": "medium",
            "status": "pending"
        }}
    ]
}}"""

    with create_loading_indicator(
        "Generating tasks with Claude..." +
        (" (via AWS Bedrock)" if config.use_bedrock else "")
    ) as progress:
        try:
            # Create message
            messages = []
            
            # Handle system prompt differently for each client type
            if isinstance(anthropic_client, AnthropicBedrock):
                # For Bedrock, include system prompt as assistant message
                messages = [
                    {
                        "role": "assistant",
                        "content": f"I understand. I will act as a technical lead and follow these instructions:\n\n{system_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"Here is the PRD content from {prd_path}:\n\n{content}"
                    }
                ]
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "messages": messages
                }
            else:
                # For direct API, use system parameter
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature,
                    "system": system_prompt,
                    "messages": [{
                        "role": "user",
                        "content": f"Here is the PRD content from {prd_path}:\n\n{content}"
                    }]
                }
            
            # Call appropriate client
            if isinstance(anthropic_client, AnthropicBedrock):
                response = anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            else:
                response = await anthropic_client.messages.create(**message_params)
                response_content = response.content[0].text
            
            # Extract JSON from response
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in Claude's response")
            
            tasks_data = json.loads(response_content[json_start:json_end])
            
            # Validate structure
            if not isinstance(tasks_data, dict) or 'tasks' not in tasks_data:
                raise ValueError("Invalid task data structure")
            
            return tasks_data
            
        except Exception as e:
            log.error(f"Error calling Claude: {e}")
            raise

async def generate_subtasks(
    task: Dict[str, Any],
    num_subtasks: int = 5,
    use_research: bool = False,
    additional_context: str = "",
    progress: Optional[Progress] = None
) -> List[Dict[str, Any]]:
    """Generate subtasks for a given task."""
    if use_research and perplexity_client:
        return await generate_subtasks_with_perplexity(
            task,
            num_subtasks,
            additional_context,
            progress
        )
    
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )
    
    system_prompt = f"""You are helping to break down a development task into smaller subtasks.
Given a task, generate {num_subtasks} specific, actionable subtasks that would be needed to complete it.

For each subtask, include:
1. A clear, specific title
2. A description
3. Implementation details
4. Dependencies on other subtasks (by ID) or the parent task

Return the subtasks as a JSON array with this structure:
[
    {{
        "id": 1,
        "title": "Subtask title",
        "description": "Subtask description",
        "details": "Implementation details",
        "dependencies": [],
        "status": "pending"
    }}
]"""

    task_content = f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""

    if additional_context:
        task_content += f"\n\nAdditional Context: {additional_context}"

    # Only create a new progress if one wasn't provided
    own_progress = False
    if progress is None:
        progress = create_loading_indicator(
            "Generating subtasks with Claude..." +
            (" (via AWS Bedrock)" if config.use_bedrock else "")
        )
        progress.start()
        own_progress = True
    
    try:
        # Create message
        if isinstance(anthropic_client, AnthropicBedrock):
            # For Bedrock, include system prompt as assistant message
            messages = [
                {
                    "role": "assistant",
                    "content": f"I understand. I will help break down the task following these instructions:\n\n{system_prompt}"
                },
                {
                    "role": "user",
                    "content": task_content
                }
            ]
            message_params = {
                "model": config.claude_model,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "messages": messages
            }
        else:
            # For direct API, use system parameter
            message_params = {
                "model": config.claude_model,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
                "system": system_prompt,
                "messages": [{
                    "role": "user",
                    "content": task_content
                }]
            }
        
        # Call appropriate client
        if isinstance(anthropic_client, AnthropicBedrock):
            response = anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        else:
            response = await anthropic_client.messages.create(**message_params)
            response_content = response.content[0].text
        
        # Extract JSON from response
        json_start = response_content.find('[')
        json_end = response_content.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in Claude's response")
        
        subtasks = json.loads(response_content[json_start:json_end])
        
        # Validate structure
        if not isinstance(subtasks, list):
            raise ValueError("Invalid subtask data structure")
        
        return subtasks
        
    except Exception as e:
        log.error(f"Error generating subtasks: {e}")
        raise
    finally:
        if own_progress:
            progress.stop()

async def generate_subtasks_with_perplexity(
    task: Dict[str, Any],
    num_subtasks: int = 5,
    additional_context: str = "",
    progress: Optional[Progress] = None
) -> List[Dict[str, Any]]:
    """Generate subtasks using Perplexity AI for research."""
    if not perplexity_client:
        raise RuntimeError(
            "Perplexity client not available. Please check your API key."
        )

    system_prompt = f"""You are a technical researcher helping to break down a development task.
Use your research capabilities to find relevant information, best practices, and implementation details.
Then generate {num_subtasks} specific, actionable subtasks based on your research.

For each subtask, include:
1. A clear, specific title
2. A description incorporating research findings
3. Detailed implementation steps based on best practices
4. Dependencies on other subtasks (by ID) or the parent task

Return the subtasks as a JSON array."""

    task_content = f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""

    if additional_context:
        task_content += f"\n\nAdditional Context: {additional_context}"

    # Only create a new progress if one wasn't provided
    own_progress = False
    if progress is None:
        progress = create_loading_indicator("Researching and generating subtasks with Perplexity...")
        progress.start()
        own_progress = True
    
    try:
        response = await perplexity_client.chat.completions.create(
            model=config.perplexity_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_content}
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content
        json_start = content.find('[')
        json_end = content.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in Perplexity's response")
        
        subtasks = json.loads(content[json_start:json_end])
        
        # Validate structure
        if not isinstance(subtasks, list):
            raise ValueError("Invalid subtask data structure")
        
        return subtasks
        
    except Exception as e:
        log.error(f"Error generating subtasks with Perplexity: {e}")
        raise
    finally:
        if own_progress:
            progress.stop()

def generate_complexity_analysis_prompt(data: Dict[str, Any]) -> str:
    """Generate a prompt for task complexity analysis."""
    tasks_content = "\n\n".join([
        f"""Task {task['id']}: {task['title']}
Description: {task['description']}
Details: {task['details']}"""
        for task in data['tasks']
    ])

    return f"""You are an expert software architect analyzing task complexity.
Please analyze each task and provide a detailed complexity assessment.

Tasks to analyze:

{tasks_content}

For each task, provide:
1. A complexity score (1-10, where 10 is most complex)
2. Recommended number of subtasks (if score >= 5)
3. A detailed expansion prompt for breaking down the task
4. Reasoning for the complexity assessment

Return your analysis as a JSON array with this structure:
[
    {{
        "taskId": 1,
        "taskTitle": "Task title",
        "complexityScore": 7,
        "recommendedSubtasks": 4,
        "expansionPrompt": "Detailed prompt for expansion",
        "reasoning": "Explanation of complexity assessment"
    }}
]

Consider:
1. Technical complexity and implementation challenges
2. Dependencies and integration points
3. Required expertise and domain knowledge
4. Testing requirements and validation complexity
5. Potential risks and edge cases
6. Estimated time investment"""

async def analyze_task_complexity(
    tasks: List[Dict[str, Any]],
    prompt: str,
    use_research: bool = False,
    model_override: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Analyze task complexity using AI."""
    if use_research and perplexity_client:
        try:
            # Add research context to prompt
            research_prompt = f"""You are conducting a detailed analysis of software development tasks.
Please research each task thoroughly, considering best practices, industry standards, and potential implementation challenges.

{prompt}

CRITICAL: You MUST respond ONLY with a valid JSON array. Do not include ANY explanatory text or markdown formatting."""

            response = await perplexity_client.chat.completions.create(
                model=config.perplexity_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical analysis AI that only responds with clean, valid JSON."
                    },
                    {
                        "role": "user",
                        "content": research_prompt
                    }
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in Perplexity's response")
            
            return json.loads(content[json_start:json_end])
            
        except Exception as e:
            log.warning(f"Perplexity analysis failed: {e}. Falling back to Claude.")
    
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )
    
    # Create message parameters
    if isinstance(anthropic_client, AnthropicBedrock):
        messages = [
            {
                "role": "assistant",
                "content": "I understand. I will analyze the tasks and provide complexity assessments."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        message_params = {
            "model": model_override or config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "messages": messages
        }
    else:
        message_params = {
            "model": model_override or config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "system": "You are an expert software architect analyzing task complexity. Respond only with valid JSON.",
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }
    
    # Call appropriate client
    if isinstance(anthropic_client, AnthropicBedrock):
        response = anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    else:
        response = await anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    
    # Extract JSON from response
    json_start = response_content.find('[')
    json_end = response_content.rfind(']') + 1
    
    if json_start == -1 or json_end == 0:
        raise ValueError("No valid JSON found in Claude's response")
    
    return json.loads(response_content[json_start:json_end])

async def generate_task_details(prompt: str) -> Dict[str, str]:
    """Generate task details using AI.
    
    Args:
        prompt: Description of the task to generate details for
    
    Returns:
        Dictionary containing task details (title, description, details, testStrategy)
    """
    if not anthropic_client:
        raise RuntimeError(
            "Claude service not available. Please configure either direct API "
            "access or AWS Bedrock."
        )
    
    system_prompt = """You are helping to create a detailed software development task.
Given a task description, generate a complete task specification including:
1. A clear, specific title
2. A detailed description
3. Implementation details
4. A test strategy

Return the task details as a JSON object with this structure:
{
    "title": "Task title",
    "description": "Task description",
    "details": "Implementation details",
    "testStrategy": "How to test this task"
}"""

    # Create message parameters
    if isinstance(anthropic_client, AnthropicBedrock):
        messages = [
            {
                "role": "assistant",
                "content": f"I understand. I will help create a task specification following these instructions:\n\n{system_prompt}"
            },
            {
                "role": "user",
                "content": f"Generate task details for: {prompt}"
            }
        ]
        message_params = {
            "model": config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "messages": messages
        }
    else:
        message_params = {
            "model": config.claude_model,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "system": system_prompt,
            "messages": [{
                "role": "user",
                "content": f"Generate task details for: {prompt}"
            }]
        }
    
    # Call appropriate client
    if isinstance(anthropic_client, AnthropicBedrock):
        response = anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    else:
        response = await anthropic_client.messages.create(**message_params)
        response_content = response.content[0].text
    
    # Extract JSON from response
    json_start = response_content.find('{')
    json_end = response_content.rfind('}') + 1
    
    if json_start == -1 or json_end == 0:
        raise ValueError("No valid JSON found in Claude's response")
    
    task_details = json.loads(response_content[json_start:json_end])
    
    # Validate structure
    required_fields = {'title', 'description', 'details', 'testStrategy'}
    if not all(field in task_details for field in required_fields):
        raise ValueError("Invalid task details structure")
    
    return task_details