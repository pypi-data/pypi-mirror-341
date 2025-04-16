### Overview

The Snowplow Signals SDK is the interface between the Feature Store (Personalisation API), the frontend JS plugin and the customer's own agentic implementation. It will extract features from the online store, and eventually handle the creation/update of features.

### JS plugin Integration

The first step is to integrate the SDK with the already prototyped JS plugin. The JS sets a `sp_signals' cookie, key value pairs as below:

```json
{
    session_count: 3,
    last_page_visited: acme.com/about,
    last_product_viewed: "Nike Red Shoes",
    first_product_viewed: "Adidas Black Shoes",
    last_product_added_to_cart: "Green Socks"
}
```

The Python sdk should have a mechanism to accept a cookie in this format, and insert it into a "feature" string. eg

```
features_from_cookie = SignalsAI.get_features_from_cookie(req.cookies)
last_visited_page = features_from_cookie.get_feature("last_page_visited")

last_visited_page_prompt = f"The last page the visitor visited was {last_visited_page}"
# The last page the visitor visited was acme.com/about

```

### Feature Retrieval

The SDK should be able to retrieve a single from teh online feature store.

An example of the Feast Python SDK is below. Pass a list of dictionarys to define which entities to retrieve, and a list of the feature view/names. This can be returned as a dictionary to access in app.

```python
# Initialize the feature store
store = FeatureStore(repo_path="path_to_your_repo")

# Specify the entity and features you want to retrieve
entity_rows = [{"entity_id": 1001}]
features = ["feature_view:feature_name"]

# Retrieve the features
feature_data = store.get_online_features(features=features, entity_rows=entity_rows).to_dict()
print(feature_data)
```

### Feature Store Integration

As per the feature store [Spike](https://www.notion.so/keep-in-the-snow/Spike-Feature-Store-API-17d07af295a280e28c80cd3533f05d09)

### Release Process

To make a new release, follow these steps:

1. **Prepare the changelog**: Create a commit (e.g., "Prepare for release") that updates the `CHANGELOG.md` with all notable changes for the new version.
2. **Create a release PR**: Open a pull request to the `main` branch with your changelog and any other release-related changes.
3. **Merge the PR**: Merge the release PR using a merge commit. _Do not use squash or rebase._
4. **Run the Release workflow**: Trigger the "Release" workflow in GitHub Actions to publish the new version to PyPI.

This process ensures a clear release history and proper automation of package publishing.
