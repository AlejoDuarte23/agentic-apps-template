# Convert VIKTOR App Params to JSON Schema

This folder contains Jupyter notebooks to extract parametrization definitions from VIKTOR apps and convert them to JSON schemas using the **VIKTOR REST API**.

## Setup

### 1. Create `.env` file

Create a `.env` file **in this directory** (`convert-app-params-to-schema/.env`) with your VIKTOR credentials:

```env
# VIKTOR Personal Access Token (starts with vktrpat_)
# For demo.viktor.ai, get it from: https://demo.viktor.ai/profile/api-tokens
# For production cloud.viktor.ai, get it from: https://cloud.viktor.ai/profile/api-tokens
#
# IMPORTANT: Paste ONLY the token value, do NOT include:
# - "Bearer " prefix
# - "Authorization:" prefix
# - Quotes or angle brackets
# - Spaces or newlines
VIKTOR_API_TOKEN=vktrpat_your_actual_token_here

# VIKTOR Environment (defaults to "demo")
# Options: "demo", "cloud", or full URL like "https://demo.viktor.ai"
VIKTOR_ENVIRONMENT=demo
```

### 2. Install dependencies

```bash
pip install requests python-dotenv
```

**Note:** These notebooks use the VIKTOR REST API directly (via `requests`) instead of the VIKTOR SDK to avoid SDK versioning and memoization issues.

### 3. Run notebooks

- **`app1_reaction_load_params.ipynb`**: Extracts schema from workspace 2672, entity 12162
- **`app2_reaction_load_params.ipynb`**: Extracts schema from workspace 2673, entity 12163

Each notebook will:
1. Connect to the VIKTOR REST API with Bearer token authentication
2. Fetch the entity with `GET /api/workspaces/{workspace_id}/entities/{entity_id}/`
3. Extract parameters from the `properties` field in the response
4. Convert it to a JSON schema with `additionalProperties: false`
5. Save the schema to a JSON file

## Output

Each notebook generates a JSON schema file that can be used for:
- OpenAI Structured Outputs
- Validation of user inputs
- Documentation generation
- Integration with other systems

## Why REST API instead of SDK?

These notebooks use the VIKTOR REST API directly to avoid:
- SDK version compatibility issues
- Internal SDK memoization errors (`api-memoize`, `KeyError: 'include_params'`)
- Environment setup complexity when running outside a VIKTOR app

The REST API provides a stable, documented interface that works consistently across environments.

## Troubleshooting

### HTTP 401 Unauthorized - "Unable to parse authentication"

Your token format is incorrect. The notebooks now validate your token and will show clear errors:

**Common mistakes:**
- ❌ `VIKTOR_API_TOKEN=Bearer vktrpat_...` (remove "Bearer ")
- ❌ `VIKTOR_API_TOKEN="vktrpat_..."` (remove quotes)
- ❌ `VIKTOR_API_TOKEN=Authorization: Bearer vktrpat_...` (remove everything before the token)
- ✅ `VIKTOR_API_TOKEN=vktrpat_7a88702c14224cc1972010e4deea8329_...` (correct!)

**Your token must:**
1. Start with `vktrpat_`
2. Be a valid Personal Access Token from https://demo.viktor.ai/profile/api-tokens
3. Have no spaces, quotes, or prefixes
4. Not be expired

**After fixing `.env`:**
1. Save the file
2. **Restart your Jupyter kernel** (Kernel → Restart)
3. Run all cells again

The notebook will show:
```
Using VIKTOR PAT: vktrpat_7a88...nnRM
Authorization header shape: Bearer vktrpat_...
```

### HTTP 403 Forbidden

Your token doesn't have permission to access the workspace/entity:
- Verify you're using the correct workspace ID
- Ensure your user has read access to the entity
- Check that the entity exists

### HTTP 404 Not Found

The workspace or entity doesn't exist:
- Verify the workspace ID and entity ID are correct
- Check the VIKTOR_ENVIRONMENT in your `.env` file matches the instance where the entity exists

### No parameters found

If `extract_saved_params()` raises a KeyError:
1. Check the raw entity response: `print(json.dumps(entity, indent=2))`
2. Verify the entity has saved parameters
3. Look for alternative keys in the response (`properties`, `params`, `last_saved_params`)
