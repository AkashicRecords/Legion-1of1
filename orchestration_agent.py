import json
import logging
import os
from datetime import datetime
from importlib import import_module
import asyncio

# Load configuration
def load_config(config_path='config.json'):
    with open(config_path, 'r') as f:
        return json.load(f)

# Initialize logging
def init_logging():
    log_filename = 'orchestration_agent.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')
    logging.info(f"Starting orchestration agent at {datetime.now()}")

# Load sub-agents
def load_sub_agents(config):
    sub_agents = {}
    for agent_name, agent_info in config['sub_agents'].items():
        module = import_module(agent_info['module'])
        class_ = getattr(module, agent_info['class'])
        sub_agents[agent_name] = class_(config)
    return sub_agents

# Delegate tasks to sub-agents
async def delegate_task(sub_agents, task, task_routing):
    data_type = task['type']
    if data_type in task_routing:
        agents = task_routing[data_type]
        tasks = [sub_agents[agent].handle_task(task) for agent in agents if agent != 'output_finalization_agent']
        await asyncio.gather(*tasks)
        # Call the output finalization agent last
        if 'output_finalization_agent' in agents:
            await sub_agents['output_finalization_agent'].handle_task(task)
    else:
        logging.error(f"No sub-agents found for data type {data_type}")

# Main function
def main():
    init_logging()
    config = load_config()
    sub_agents = load_sub_agents(config)
    task_routing = config['task_routing']
    
    # Example task delegation
    task = {
        'type': 'text',
        'data': 'Sample data to ingest'
    }
    asyncio.run(delegate_task(sub_agents, task, task_routing))

if __name__ == "__main__":
    main()