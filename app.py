import os
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ['SLACK_BOT_TOKEN'],
    signing_secret=os.environ['SLACK_SIGNING_SECRET']
)


@app.command("/test")
def open_create_issue_model(ack, body, client):

    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view_1",
            "title": {
                "type": "plain_text",
                "text": "Stage Stability Bot",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Create",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Creat a new Stage issue* :bug:"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "issue_description_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "issue_description"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Issue Description",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "reported_to_block",
                    "element": {
                            "type": "multi_users_select",
                        "placeholder": {
                                    "type": "plain_text",
                            "text": "Select assignee",
                            "emoji": True
                        },
                        "action_id": "reported_to"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Reported To",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "impacted_services_block",
                    "element": {
                        "type": "multi_users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select imapcted services",
                            "emoji": True
                        },
                        "action_id": "impacted_services"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Impacted Services",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "debug_data_block",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "debug_data"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Debug Data [Request, Response, transaction ids etc]",
                        "emoji": True
                    }
                }
            ]
        }
    )

@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    print("Inside view method ...")
    # Assume there's an input block with `input_c` as the block_id and `dreamy_input`
    issue_description = view["state"]["values"]["issue_description_block"]["issue_description"]
    reported_to = view["state"]["values"]["reported_to_block"]["reported_to"]
    impacted_services = view["state"]["values"]["impacted_services_block"]["impacted_services"]
    debug_data = view["state"]["values"]["debug_data_block"]["debug_data"]
    user = body["user"]["id"]
    # Validate the inputs
    errors = {}
    # if hopes_and_dreams is not None and len(hopes_and_dreams) <= 5:
    #     errors["input_c"] = "The value must be longer than 5 characters"
    # if len(errors) > 0:
    #     ack(response_action="errors", errors=errors)
    #     return
    # Acknowledge the view_submission request and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission

    # Message to send user
    msg = ""
    try:
        # Save to DB
        msg = f"Issue : {issue_description['value']}"
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    try:
        client.chat_postMessage(channel="#testing-bots", text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        logger.info(event)
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me!"
                                }
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 5000)))
