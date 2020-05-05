# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from matplotlib import pyplot as plt


#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionRespondCoroanStateCity(Action):
    def name(self):
        return "action_corona_state"

    def run(self, dispatcher, tracker, domain):
        # last_message = tracker.latest_message.get("text", "")

        response = requests.get("https://api.covid19india.org/data.json").json()
        print("Length ", len(response["statewise"]))
        message = "Please enter correct STATE name"

        entities = tracker.latest_message['entities']
        print("Last Message Now  and its user entered entity", entities)
        state = None
        for e in entities:
            if e['entity'] == "state":
                state = e['value']

        print("State ", state)
        # state = state.lower()
        print("State ", state)
        if state == "corona":
            state = "Total"
        if state == "india":
            state = "Total"

            # print("State ", state.title())
        message = "Please enter correct STATE name"
        if (state != None):
            message = "Please enter correct STATE name"
            for data in response["statewise"]:
                if data["state"] == state.title():
                    print(data)
                    message = "Active: " + data["active"] + " Confirmed: " + data["confirmed"] + " Recovered: " + data[
                        "recovered"] + " On " + data["lastupdatedtime"]


                    active = data["active"]
                    Confirmed = data["confirmed"]
                    Recovered = data["recovered"]
                    as_on = data["lastupdatedtime"]
                    #for date visualization part
                    fig = plt.figure()
                    ax = fig.add_axes([0,0,1,1])
                    ax.axis('equal')
                    langs = ['Active', 'Confirmed', 'Recovered']
                    students = [active,Confirmed  , Recovered]
                    ax.pie(students, labels=langs, autopct='%1.2f%%')
                    plt.savefig("test.png")
                    image_growth_up= "test.png"

                    dispatcher.utter_template("utter_pie_image", tracker, image_growth_up=image_growth_up)
        dispatcher.utter_message(message)

        return []


class Say_name(Action):
    def name(self) -> Text:
        return "action_say_name"
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities= tracker.latest_message["entities"]
        print("your entity is ", entities)
        for e in entities:
            say_name = e['value']
            print("ur name", say_name)
            dispatcher.utter_template("action_say_name", tracker, say_name=say_name)


        #dispatcher.utter_message(say_name)

        return []