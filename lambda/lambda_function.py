# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
from utils import create_presigned_url, rabbitmq_test
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

# import boto3
# import botocore
# import paramiko
# import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, to smarter home, you can give command or Help. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class turnIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("turn")(handler_input)
        
    def gen_out(self,device_name,status,id1,status_id):
        try:
            speak_output = device_name +" is "+status
            
            try:
                rabbitmq_test("device",[int(id1),int(status_id),None])
            except:
                speak_output = "connection to rabbitMQ failed"
                
        except:
            speak_output = "turning " + status +" "+ device_name  + " failed!"
        return(speak_output)
        
    def gen_out2(self,type_name,status,id1,status_id,zone_id):
        try:
            speak_output = type_name +" is "+status
            
            try:
                rabbitmq_test("types",[int(id1),int(status_id),zone_id])
            except:
                speak_output = "connection to rabbitMQ failed"
                
        except:
            speak_output = "turning " + status +" "+ type_name  + " failed!"
        return(speak_output)
        
    def handle(self,handler_input):
        slots = handler_input.request_envelope.request.intent.slots 
        speak_output = str(slots["device_name"])
        if(slots["status"].value):
            status = (slots["status"].value)
            status_id = slots["status"].resolutions.resolutions_per_authority[0].values[0].value.id
        else:
            status = "ON"
            status_id = 1
        if(slots["numbers"].value):
            status_id = int(slots["numbers"].resolutions.resolutions_per_authority[0].values[0].value.id)
        if(slots["zone"].value):
            zone_name = ' in '+str(slots["zone"].value)
            zone_id = int(slots["zone"].resolutions.resolutions_per_authority[0].values[0].value.id)
        else:
            zone_name = ''
            zone_id = None
        
        if(slots["device_name"].value):
            device_name = (slots["device_name"].value)
            device_id = slots["device_name"].resolutions.resolutions_per_authority[0].values[0].value.id
            speak_output = self.gen_out(device_name,status,device_id,status_id)
        else:
            device_name=None
        if(slots["types"].value):
            type_name = (slots["types"].value)
            type_id = slots["types"].resolutions.resolutions_per_authority[0].values[0].value.id
            speak_output = self.gen_out2(type_name,status,type_id,status_id,zone_id)
        else:
            type_name = None
        
        speak_output = speak_output+zone_name
        return(handler_input.response_builder
        .speak(speak_output)
        .ask(speak_output)
        .response)
        

class sceneIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("scenes")(handler_input)
    def handle(self,handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        parameter=0
        if(slots["status"].value):
            status = (slots["status"].value)
            status_id = slots["status"].resolutions.resolutions_per_authority[0].values[0].value.id
        else:
            status = "START"
            status_id = 3
        if(slots["scene"].value):
            scene_name = (slots["scene"].value)
            scene_id = slots["scene"].resolutions.resolutions_per_authority[0].values[0].value.id
        else:
            device_name=None
        
        try:
            # scene_name = (slots["scene"].value)
            scene_status = status
            # id1 = slots["scene"].resolutions.resolutions_per_authority[0].values[0].value.id
            # try:
            #     scene_status = (slots["status"].value)
            # except:
            #     scene_status = None
            # if(scene_status==None):
            #     speak_output = scene_name+" is initiating "
            #     parameter=1
            if(scene_status=='start'):
                speak_output = scene_name+" is initiating"
                parameter=1
            elif(scene_status=='stop'):
                speak_output = scene_name+" is terminating"
                parameter=0
            try:
                rabbitmq_test("scene",[int(scene_id),parameter,None])
            except:
                speak_output = "connection to rabbitMQ failed"
                
        except:
            speak_output = "initiating " +" "+ scene_name  + " failed!"
        return(handler_input.response_builder
        .speak(speak_output)
        .ask(speak_output)
        .response)

class sceneZoneIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("scene")(handler_input)
    def handle(self,handler_input):
        
        try:
            slots = handler_input.request_envelope.request.intent.slots 
            scene_name = (slots["scenes"].value)
            zone_name = (slots["zone_name"].value)
            speak_output = scene_name+" is initiating in "+zone_name
            
            try:
                rabbitmq_test()
            except:
                speak_output = "connection to rabbitMQ failed"
                
        except:
            speak_output = "initiating " +" "+ scene_name  +" in " + " failed!"
        return(handler_input.response_builder
        .speak(speak_output)
        .ask(speak_output)
        .response)

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speak_output = "You can say hello to me! How can I help?"
        speak_output = "to turn on light in living room, just say turn on living room light"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(turnIntentHandler())
sb.add_request_handler(sceneIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()