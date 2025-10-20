# List tasks

GET http://localhost:8000/api/tasks/

Retrieve a paginated list of tasks. The response format varies based on the user's role in the organization:
- **Admin/Owner**: Full task details with all annotations, reviews, and metadata
- **Reviewer**: Task details optimized for review workflow
- **Annotator**: Task details filtered to show only user's own annotations and assignments

Reference: https://api.labelstud.io/api-reference/api-reference/tasks/list

## OpenAPI Specification

```yaml
openapi: 3.1.1
info:
  title: List tasks
  version: endpoint_tasks.list
paths:
  /api/tasks/:
    get:
      operationId: list
      summary: List tasks
      description: >-
        Retrieve a paginated list of tasks. The response format varies based on
        the user's role in the organization:

        - **Admin/Owner**: Full task details with all annotations, reviews, and
        metadata

        - **Reviewer**: Task details optimized for review workflow

        - **Annotator**: Task details filtered to show only user's own
        annotations and assignments
      tags:
        - - subpackage_tasks
      parameters:
        - name: fields
          in: query
          description: >-
            Set to "all" if you want to include annotations and predictions in
            the response. Defaults to task_only
          required: false
          schema:
            $ref: '#/components/schemas/type_tasks:TasksListRequestFields'
        - name: include
          in: query
          description: Specify which fields to include in the response
          required: false
          schema:
            type: string
        - name: only_annotated
          in: query
          description: Filter to show only tasks that have annotations
          required: false
          schema:
            type: boolean
        - name: page
          in: query
          description: A page number within the paginated result set.
          required: false
          schema:
            type: integer
        - name: page_size
          in: query
          description: Number of results to return per page.
          required: false
          schema:
            type: integer
        - name: project
          in: query
          description: Project ID
          required: false
          schema:
            type: integer
        - name: query
          in: query
          description: >-
            Additional query to filter tasks. It must be JSON encoded string of
            dict containing one of the following parameters: {"filters": ...,
            "selectedItems": ..., "ordering": ...}. Check Data Manager > Create
            View > see data field for more details about filters, selectedItems
            and ordering.


            filters: dict with "conjunction" string ("or" or "and") and list of
            filters in "items" array. Each filter is a dictionary with keys:
            "filter", "operator", "type", "value". Read more about available
            filters

            Example: {"conjunction": "or", "items": [{"filter":
            "filter:tasks:completed_at", "operator": "greater", "type":
            "Datetime", "value": "2021-01-01T00:00:00.000Z"}]}

            selectedItems: dictionary with keys: "all", "included", "excluded".
            If "all" is false, "included" must be used. If "all" is true,
            "excluded" must be used.

            Examples: {"all": false, "included": [1, 2, 3]} or {"all": true,
            "excluded": [4, 5]}

            ordering: list of fields to order by. Currently, ordering is
            supported by only one parameter.

            Example: ["completed_at"]
          required: false
          schema:
            type: string
        - name: resolve_uri
          in: query
          description: Resolve task data URIs using Cloud Storage
          required: false
          schema:
            type: boolean
        - name: review
          in: query
          description: Get tasks for review
          required: false
          schema:
            type: boolean
        - name: selectedItems
          in: query
          description: JSON string of selected task IDs for review workflow
          required: false
          schema:
            type: string
        - name: view
          in: query
          description: View ID
          required: false
          schema:
            type: integer
        - name: Authorization
          in: header
          description: Header authentication of the form `Token  <token>`
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Response with status 200
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/type_:PaginatedRoleBasedTaskList'
        '400':
          description: Bad request - invalid parameters
          content: {}
        '401':
          description: Unauthorized - authentication required
          content: {}
        '403':
          description: Forbidden - insufficient permissions
          content: {}
components:
  schemas:
    type_tasks:TasksListRequestFields:
      type: string
      enum:
        - value: all
        - value: task_only
    type_:LseTaskDraftsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        updated_at:
          type: string
          format: date-time
    type_:LseTaskPredictionsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        model:
          type: object
          additionalProperties:
            description: Any type
        model_run:
          type: object
          additionalProperties:
            description: Any type
        model_version:
          type: string
        project:
          type: integer
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        score:
          type: number
          format: double
        task:
          type: integer
        updated_at:
          type: string
          format: date-time
    type_:LseTask:
      type: object
      properties:
        agreement:
          type: string
        agreement_selected:
          type: string
        annotations:
          type: string
        annotations_ids:
          type: string
        annotations_results:
          type: string
        annotators:
          type: array
          items:
            type: integer
        annotators_count:
          type: integer
        avg_lead_time:
          type: number
          format: double
        cancelled_annotations:
          type: integer
        comment_authors:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        comment_authors_count:
          type: integer
        comment_count:
          type: integer
        comments:
          type: string
        completed_at:
          type: string
          format: date-time
        created_at:
          type: string
          format: date-time
        data:
          description: Any type
        draft_exists:
          type: boolean
        drafts:
          type: array
          items:
            $ref: '#/components/schemas/type_:LseTaskDraftsItem'
        file_upload:
          type: string
        ground_truth:
          type: boolean
        id:
          type: integer
        inner_id:
          type: integer
        is_labeled:
          type: boolean
        last_comment_updated_at:
          type: string
          format: date-time
        meta:
          description: Any type
        overlap:
          type: integer
        predictions:
          type: array
          items:
            $ref: '#/components/schemas/type_:LseTaskPredictionsItem'
        predictions_model_versions:
          type: string
        predictions_results:
          type: string
        predictions_score:
          type: number
          format: double
        project:
          type: integer
        review_time:
          type: integer
        reviewed:
          type: boolean
        reviewers:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        reviewers_count:
          type: integer
        reviews_accepted:
          type: integer
        reviews_rejected:
          type: integer
        storage_filename:
          type: string
        total_annotations:
          type: integer
        total_predictions:
          type: integer
        unresolved_comment_count:
          type: integer
        updated_at:
          type: string
          format: date-time
        updated_by:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
      required:
        - agreement
        - agreement_selected
        - annotations
        - annotations_ids
        - annotations_results
        - annotators
        - annotators_count
        - comment_authors
        - comment_authors_count
        - comments
        - created_at
        - data
        - drafts
        - file_upload
        - id
        - predictions
        - predictions_model_versions
        - predictions_results
        - review_time
        - reviewers
        - reviewers_count
        - storage_filename
        - updated_at
        - updated_by
    type_:LseTaskSerializerForReviewersDraftsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        updated_at:
          type: string
          format: date-time
    type_:LseTaskSerializerForReviewersPredictionsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        model:
          type: object
          additionalProperties:
            description: Any type
        model_run:
          type: object
          additionalProperties:
            description: Any type
        model_version:
          type: string
        project:
          type: integer
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        score:
          type: number
          format: double
        task:
          type: integer
        updated_at:
          type: string
          format: date-time
    type_:LseTaskSerializerForReviewers:
      type: object
      properties:
        agreement:
          type: string
        agreement_selected:
          type: string
        annotations:
          type: string
        annotations_ids:
          type: string
        annotations_results:
          type: string
        annotators:
          type: array
          items:
            type: integer
        annotators_count:
          type: integer
        avg_lead_time:
          type: number
          format: double
        cancelled_annotations:
          type: integer
        comment_authors:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        comment_authors_count:
          type: integer
        comment_count:
          type: integer
        comments:
          type: string
        completed_at:
          type: string
          format: date-time
        created_at:
          type: string
          format: date-time
        data:
          description: Any type
        draft_exists:
          type: boolean
        drafts:
          type: array
          items:
            $ref: '#/components/schemas/type_:LseTaskSerializerForReviewersDraftsItem'
        file_upload:
          type: string
        ground_truth:
          type: boolean
        id:
          type: integer
        inner_id:
          type: integer
        is_labeled:
          type: boolean
        last_comment_updated_at:
          type: string
          format: date-time
        meta:
          description: Any type
        overlap:
          type: integer
        predictions:
          type: array
          items:
            $ref: >-
              #/components/schemas/type_:LseTaskSerializerForReviewersPredictionsItem
        predictions_model_versions:
          type: string
        predictions_results:
          type: string
        predictions_score:
          type: number
          format: double
        project:
          type: integer
        review_time:
          type: integer
        reviewed:
          type: boolean
        reviewers:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        reviewers_count:
          type: integer
        reviews_accepted:
          type: integer
        reviews_rejected:
          type: integer
        storage_filename:
          type: string
        total_annotations:
          type: integer
        total_predictions:
          type: integer
        unresolved_comment_count:
          type: integer
        updated_at:
          type: string
          format: date-time
        updated_by:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
      required:
        - agreement
        - agreement_selected
        - annotations
        - annotations_ids
        - annotations_results
        - annotators
        - annotators_count
        - comment_authors
        - comment_authors_count
        - comments
        - created_at
        - data
        - drafts
        - file_upload
        - id
        - predictions
        - predictions_model_versions
        - predictions_results
        - review_time
        - reviewers
        - reviewers_count
        - storage_filename
        - updated_at
        - updated_by
    type_:LseTaskSerializerForAnnotatorsDraftsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        updated_at:
          type: string
          format: date-time
    type_:LseTaskSerializerForAnnotatorsPredictionsItem:
      type: object
      properties:
        created_at:
          type: string
          format: date-time
        model:
          type: object
          additionalProperties:
            description: Any type
        model_run:
          type: object
          additionalProperties:
            description: Any type
        model_version:
          type: string
        project:
          type: integer
        result:
          type: array
          items:
            type: object
            additionalProperties:
              description: Any type
        score:
          type: number
          format: double
        task:
          type: integer
        updated_at:
          type: string
          format: date-time
    type_:LseTaskSerializerForAnnotators:
      type: object
      properties:
        annotations:
          type: string
        annotations_results:
          type: string
        cancelled_annotations:
          type: integer
        comment_count:
          type: string
        comments:
          type: string
        created_at:
          type: string
          format: date-time
        data:
          description: Any type
        draft_exists:
          type: boolean
        drafts:
          type: array
          items:
            $ref: >-
              #/components/schemas/type_:LseTaskSerializerForAnnotatorsDraftsItem
        id:
          type: integer
        predictions:
          type: array
          items:
            $ref: >-
              #/components/schemas/type_:LseTaskSerializerForAnnotatorsPredictionsItem
        predictions_results:
          type: string
        predictions_score:
          type: number
          format: double
        reviews_rejected:
          type: integer
        total_annotations:
          type: integer
        total_predictions:
          type: integer
        unresolved_comment_count:
          type: string
      required:
        - annotations
        - annotations_results
        - comment_count
        - comments
        - created_at
        - data
        - drafts
        - id
        - predictions
        - predictions_results
        - unresolved_comment_count
    type_:RoleBasedTask:
      oneOf:
        - $ref: '#/components/schemas/type_:LseTask'
        - $ref: '#/components/schemas/type_:LseTaskSerializerForReviewers'
        - $ref: '#/components/schemas/type_:LseTaskSerializerForAnnotators'
    type_:PaginatedRoleBasedTaskList:
      type: object
      properties:
        tasks:
          type: array
          items:
            $ref: '#/components/schemas/type_:RoleBasedTask'
        total:
          type: integer
        total_annotations:
          type: integer
        total_predictions:
          type: integer
      required:
        - tasks
        - total
        - total_annotations
        - total_predictions

```

## SDK Code Examples

```python
from label_studio_sdk import LabelStudio

client = LabelStudio(
    api_key="YOUR_API_KEY",
)
response = client.tasks.list()
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```

```javascript
const url = 'http://localhost:8000/api/tasks/';
const options = {method: 'GET', headers: {Authorization: 'Token  <api_key>'}};

try {
  const response = await fetch(url, options);
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error(error);
}
```

```go
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "http://localhost:8000/api/tasks/"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("Authorization", "Token  <api_key>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:8000/api/tasks/")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Get.new(url)
request["Authorization"] = 'Token  <api_key>'

response = http.request(request)
puts response.read_body
```

```java
HttpResponse<String> response = Unirest.get("http://localhost:8000/api/tasks/")
  .header("Authorization", "Token  <api_key>")
  .asString();
```

```php
<?php

$client = new \GuzzleHttp\Client();

$response = $client->request('GET', 'http://localhost:8000/api/tasks/', [
  'headers' => [
    'Authorization' => 'Token  <api_key>',
  ],
]);

echo $response->getBody();
```

```csharp
var client = new RestClient("http://localhost:8000/api/tasks/");
var request = new RestRequest(Method.GET);
request.AddHeader("Authorization", "Token  <api_key>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = ["Authorization": "Token  <api_key>"]

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:8000/api/tasks/")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```