import json
import requests

# This functions prints the responses to all of the common errors the program may encounter.
def URLstatusResponder(errorCode, pageTitle):
    # Each error code case is matched with the proper response for the error and page.
    # See the text for which error is which.
    match errorCode:
        case 200:
            response = "Successful."
        case 400:
            response = "A bad request was issued for " + pageTitle + " (400)."
        case 401:
            response = "The client is unauthenticated (401)."
        case 403:
            response = "The client is forbidden from accessing the page " + pageTitle + " (403)."
        case 404:
            response = "The page for " + pageTitle + " either can't be found or no longer exists (404)."
        case 418:
            response = "The server is a teapot and refuses to brew coffee."
        case 500:
            response = "The server has run into an Internal Server Error (500)."
        case 502:
            response = "Bad gateway. Server likely got an invalid response somwehere for " + pageTitle + " (502)."
        case 503:
            response = "The server isn't ready to handle the request (503)."
        case _:
            response = "Something unusual happened. Here's the error code (" + str(errorCode) + ") for the page " + pageTitle + "."
    
    # Returns the text for the response.
    return response


# Collects and returns the JSON data present at the given link.
def URLcollector(api_URL, pageTitle):
    responseText = requests.get(api_URL)

    # In event that there is an error in retrieving the data from the API, try again once. 
    if(responseText.status_code != 200):
        responseText = requests.get(api_URL)

    # Checks response status code. If it is not successful, returns an error message with the status.
    if(responseText.status_code == 200):
        # Load the web response into a JSON data structure.
        dataJSON = json.loads(json.dumps(responseText.json()))
    else:
        # Stops further blocks from executing, preventing downstream errors.
        # Sends a short text description of the error and the returned code.
        raise SystemExit(URLstatusResponder(responseText.status_code, pageTitle))
    
    return dataJSON