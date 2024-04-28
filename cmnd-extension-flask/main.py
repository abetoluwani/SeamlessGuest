from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from flask_cors import CORS
from tools import tools
from playground.api.property.property import app as property_routes
from playground.api.payments.payments import app as payment_routes

# Load environment variables
load_dotenv()

#  init db
import services.firebase.firebase as firebase

# # playground
#import playground.test as test

# import playground.tests.payment as paystack_test

app = Flask(__name__)
CORS(app)

@app.route("/cmnd-tools", methods=['GET'])
def cmnd_tools_endpoint():
    tools_response = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool.get("isDangerous", False),
            "functionType": tool["functionType"],
            "isLongRunningTool": tool.get("isLongRunningTool", False),
            "rerun": tool["rerun"],
            "rerunWithDifferentParameters": tool["rerunWithDifferentParameters"],
        } for tool in tools
    ]
    return jsonify({"tools": tools_response})


@app.route("/run-cmnd-tool", methods=['POST'])
def run_cmnd_tool_endpoint():
    data = request.json
    tool_name = data.get('toolName')
    props = data.get('props', {})
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        abort(404, description="Tool not found")
    try:
        result = tool["runCmd"](**props)
        return jsonify(result)
    except Exception as e:
        abort(500, description=str(e))

app.register_blueprint(property_routes, url_prefix='/property')
app.register_blueprint(payment_routes, url_prefix='/payments')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)