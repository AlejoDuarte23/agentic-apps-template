# Convert VIKTOR App Params to JSON Schema

This folder contains Jupyter notebooks to extract parametrization values from VIKTOR entities and convert them to JSON schemas using the **VIKTOR REST API**.

## Setup

### 1. Create `.env` file

Create a `.env` file **in this directory** (`convert-app-params-to-schema/.env`) with your VIKTOR credentials:

```env
# VIKTOR Personal Access Token
# For demo.viktor.ai, get it from: https://demo.viktor.ai/profile/api-tokens
# For production cloud.viktor.ai, get it from: https://cloud.viktor.ai/profile/api-tokens
#
# IMPORTANT: Paste ONLY the token value, do NOT include:
# - "Bearer " prefix
# - "Authorization:" prefix
# - Quotes or angle brackets
# - Spaces or newlines
TOKEN_VK_APP=vktrpat_your_actual_token_here

# Backwards-compatible alternatives also accepted:
# VIKTOR_TOKEN=vktrpat_your_actual_token_here
# VIKTOR_API_TOKEN=vktrpat_your_actual_token_here

# VIKTOR Environment (defaults to "demo")
# Options: "demo", "cloud", or full URL like "https://demo.viktor.ai"
VIKTOR_ENVIRONMENT=demo

# Optional: use a full API base instead of an environment slug
# VIKTOR_API_BASE=https://demo.viktor.ai/api
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
1. Connect to the VIKTOR REST API with Bearer token authentication without printing the token
2. Fetch the entity with `GET /api/workspaces/{workspace_id}/entities/{entity_id}/`
3. Extract parameters from the `properties` field in the response
4. Fetch available controller methods from `entity_type.views` and parametrization actions
5. Convert saved params to a JSON schema with `additionalProperties: false`
6. Save the schema and available methods to JSON files

## Output

Each notebook generates a JSON schema file and an available-methods file:

- `app1_params_schema.json`
- `app1_available_methods.json`
- `app2_params_schema.json`
- `app2_available_methods.json`

The schema files can be used for:
- OpenAI Structured Outputs
- Validation of user inputs
- Documentation generation
- Integration with other systems

The available-methods files list callable view/action methods with labels and source metadata.

## Why REST API instead of SDK?

These notebooks use the VIKTOR REST API directly to avoid:
- SDK version compatibility issues
- Internal SDK memoization errors (`api-memoize`, `KeyError: 'include_params'`)
- Environment setup complexity when running outside a VIKTOR app

The REST API provides a stable, documented interface that works consistently across environments.

## Troubleshooting

### HTTP 401 Unauthorized - "Unable to parse authentication"

Your token format is incorrect. The notebooks validate your token shape and show clear errors without printing the token.

**Common mistakes:**
- Wrong: `TOKEN_VK_APP=Bearer vktrpat_...` (remove `Bearer `)
- Wrong: `TOKEN_VK_APP="vktrpat_..."` (remove quotes)
- Wrong: `TOKEN_VK_APP=Authorization: Bearer vktrpat_...` (remove everything before the token)
- Correct: `TOKEN_VK_APP=vktrpat_your_actual_token_here`

**Your token must:**
1. Be a valid Personal Access Token from the matching VIKTOR environment
2. Have no spaces, quotes, or prefixes
3. Not be expired

**After fixing `.env`:**
1. Save the file
2. **Restart your Jupyter kernel** (Kernel > Restart)
3. Run all cells again

The notebook will show:
```
Using VIKTOR token from environment variable: TOKEN_VK_APP
REST API base URL: https://demo.viktor.ai/api
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
