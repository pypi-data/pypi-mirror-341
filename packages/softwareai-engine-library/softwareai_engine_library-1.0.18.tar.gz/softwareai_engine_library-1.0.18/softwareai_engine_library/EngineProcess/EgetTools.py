import requests
import yaml
import os
import json
def EgetTools(tools_name_str = "autoapprovepullrequest,autochangesrequestedinpullrequest,autoconversationpullrequest"
              
    ):

    def format_tool(tool):
        return {
            "function": {
                "name": tool["id"],
                "description": tool["fullDescription"].replace("\n", "").replace("", ""),
                "parameters": tool["parameters"]
            },
            
        }

    tool_ids = [name.strip() for name in tools_name_str.split(',')]

    # Pega ferramentas via API
    response = requests.post('https://softwareai-library-hub.rshare.io/api/get-tools-by-id', json={"tool_ids": tool_ids})
    tools_data = response.json()

    # Formata cada ferramenta no formato de função
    formatted_tools = [format_tool(tool) for tool in tools_data]
    return formatted_tools, json.dumps(formatted_tools, indent=2)


# tools_name_str = "autosave,send_to_webhook_func,autopullrequest"
# Tools_Name_dict, Tools_Name_str = EgetTools(tools_name_str)
# print(Tools_Name_dict)
# print(Tools_Name_str)
