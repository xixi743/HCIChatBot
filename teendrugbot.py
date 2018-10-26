#!/usr/bin/env python3
"""A tag-based chatbot framework."""

import re
from collections import Counter

class ChatBot:
    """A tag-based chatbot framework

        This class is not meant to be instantiated. Instead, it provides helper
        functions that subclasses could use to create a tag-based chatbot. There
        are two main components to a chatbot:

        * A set of STATES to determine the context of a message.
        * A set of TAGS that match on words in the message.

        Subclasses must implement two methods for every state (except the
        default): the `on_enter_*` method and the `respond_from_*` method. For
        example, if there is a state called "confirm_delete", there should be two
        methods `on_enter_confirm_delete` and `respond_from_confirm_delete`.

        * on_enter_*()` is what the chatbot should say when it enters a state.
        This method takes no arguments, and returns a string that is the
        chatbot's response. For example, a bot might enter the "confirm_delete"
        state after a message to delete a reservation, and the
        `on_enter_confirm_delete` might return "Are you sure you want to
        delete?".

        * `respond_from_*()` determines which state the chatbot should enter next.
        It takes two arguments: a string `message`, and a dictionary `tags`
        which counts the number of times each tag appears in the message. This
        function should always return with calls to either `go_to_state` or
        `finish`.

        The `go_to_state` method automatically calls the related `on_enter_*`
        method before setting the state of the chatbot. The `finish` function calls
        a `finish_*` function before setting the state of the chatbot to the
        default state.

        The TAGS class variable is a dictionary whose keys are words/phrases and
        whose values are (list of) tags for that word/phrase. If the words/phrases
        match a message, these tags are provided to the `respond_from_*` methods.
        """

    STATES = []
    TAGS = {}

    def __init__(self, default_state):
        """Initialize a Chatbot.

        Arguments:
            default_state (str): The starting state of the agent.
        """
        if default_state not in self.STATES:
            print(' '.join([
                f'WARNING:',
                f'The default state {default_state} is listed as a state.',
                f'Perhaps you mean {self.STATES[0]}?',
            ]))
        self.default_state = default_state
        self.state = self.default_state
        self.tags = {}
        self._check_states()
        self._check_tags()

    def _check_states(self):
        """Check the STATES to make sure that relevant functions are defined."""
        for state in self.STATES:
            prefixes = []
            if state != self.default_state:
                prefixes.append('on_enter')
            prefixes.append('respond_from')
            for prefix in prefixes:
                if not hasattr(self, f'{prefix}_{state}'):
                    print(' '.join([
                        f'WARNING:',
                        f'State "{state}" is defined',
                        f'but has no response function self.{prefix}_{state}',
                    ]))

    def _check_tags(self):
        """Check the TAGS to make sure that it has the correct format."""
        for phrase in self.TAGS:
            tags = self.TAGS[phrase]
            if isinstance(tags, str):
                self.TAGS[phrase] = [tags]
            tags = self.TAGS[phrase]
            assert isinstance(tags, (tuple, list)), ' '.join([
                'ERROR:',
                'Expected tags for {phrase} to be str or List[str]',
                f'but got {tags.__class__.__name__}',
            ])

    def go_to_state(self, state):
        """Set the chatbot's state after responding appropriately.

        Arguments:
            state (str): The state to go to.

        Returns:
            str: The response of the chatbot.
        """
        assert state in self.STATES, f'ERROR: state "{state}" is not defined'
        assert state != self.default_state, ' '.join([
            'WARNING:',
            f"do not call `go_to_state` on the default state {self.default_state};",
            f'use `finish` instead',
        ])
        on_enter_method = getattr(self, f'on_enter_{state}')
        response = on_enter_method()
        self.state = state
        return response

    def chat(self):
        """Start a chat with the chatbot."""
        try:
            message = input("So, you think your teen is doing drugs? What symptoms are they exhibiting? Any changes in behvaior? \n")
            while message.lower() not in ('exit', 'quit'):
                print()
                print(f'{self.__class__.__name__}: {self.respond(message)}')
                print()
                message = input('> ')
        except (EOFError, KeyboardInterrupt):
            print()
            exit()

    def respond(self, message):
        """Respond to a message.

        Arguments:
            message (str): The message from the user.

        Returns:
            str: The response of the chatbot.
        """
        respond_method = getattr(self, f'respond_from_{self.state}')
        return respond_method(message, self._get_tags(message))

    def finish(self, manner):
        """Set the chatbot back to the default state

        This function will call the appropriate `finish_*` method.

        Arguments:
            manner (str): The type of exit from the flow.

        Returns:
            str: The response of the chatbot.
        """
        response = getattr(self, f'finish_{manner}')()
        self.state = self.default_state
        return response

    def _get_tags(self, message):
        """Find all tagged words/phrases in a message.

        Arguments:
            message (str): The message from the user.

        Returns:
            Dict[str, int]: A count of each tag found in the message.
        """
        counter = Counter()
        msg = message.lower()
        for phrase, tags in self.TAGS.items():
            if re.search(r'\b' + phrase.lower() + r'\b', msg):
                counter.update(tags)
        return counter


class teendrugbot(ChatBot):
    """A simple chatbot that directs students to office hours of CS professors."""

    STATES = [
        'waiting',
        'unknown_drug',
        'common_symptom',
        'identified_drug',
        'solution'
    ]

    TAGS = {
        # left a few example tags so I don't forget how to do them.
        # a problem we will likely encounter is that many of the drugs share symptoms
        # to avoid having a hard time identifying soley based of tags, we can make a category
        # of common symptoms and then ask leading questions based of that to further identify
        # the drug to then give advice

        # refer to "Drugs Ledger" Google Doc for all of the drugs we are adding to our dictionary

        # weed
        'red eyes': 'weed',
        'bloodshot eyes': 'weed',
        'slow reaction time': 'weed',
        'slow reaction': 'weed',
        'bad problem solving': 'weed',
        'poor problem solving': 'weed',
        'difficulty problem solving':'weed',
        'lose track of thoughts': 'weed',
        'bad memory': 'weed',
        'poor memory': 'weed',
        'short term memory':'weed',
        'extreme hunger':'weed',
        'unusual hunger': 'weed',
        'increasing eating':'weed',
        'eating more':'weed',
        'munchies':'weed',
        'silly':'weed',
        'giggly':'weed',
        'acting slow':'weed',
        'lethargic':'weed',
        'dazed':'weed',
        'confused':'weed',
        '420':'weed',
        'rolling paper':'weed',
        'bong':'weed',
        'decorative piece':'weed',
        'plants':'weed',
        'dried plant':'weed',
        'dried plants':'weed',
        'grinder':'weed'
        'oregano':'weed',
        'marijuana leaves':'weed',
        'devil':'weed',
        'devils lettuce':'weed',
        'grass':'weed',
        'cannabis':'weed',
        'blaze':'weed',
        'ganga':'weed',
        'joint':'weed',
        'blunt':'weed',
        'hemp':'weed',

        # adderall
        'headache':'addy',
        'hoarseness':'addy',
        'shaking':'addy',
        'shakiness':'addy',
        'tremors':'addy',
        'seizures':'addy',

        # common symptoms
        # I was thinking for the common symptoms that we would just say,
        # sorry, that is a common symptom,
        # and then ask a bunch of questions of symptoms to narrow it down,
        # basically 'are their eyes red?'
        # if not, next question, if yes, weed
        'cough': 'common', #shared between weed and tobacco
        'fast heartbeat':'common', #shared between adderall and weed
        'rapid heartbeat':'common',
        'dry mouth':'common', #shared in four categories
        'poor coordination': 'common', #shared between alcohol and weed
        'loss of motivation': 'common', #shared between weed and narcotics
        'no motivation': 'common',
        'lack of motivation': 'common',
        'no enthusiasm': 'common', #shared between weed and narcotics
        'loss of enthusiasm':'common',
        'lack of enthusiasm':'common',
        'paranoia':'common', #shared between weed and hallucinogens
        'paranoid':'common',
        'small baggies':'common', #cocaine, weed, narcotics, and adderall
        'pipe':'common', #narcostics, tabacco, weed
        'pipes':'common',
        'baggies':'common', #shared between weed, adderall, cocaine, and narcotics
        'small baggies':'common',
        'insence':'common', #used to mask smoking
        'air freshener':'common',
        'cologne':'common',
        'perfume':'common',
        'mouthwash':'common',
        'mints':'common',
        'gum':'common',
        'towel':'common', #towel under door to block smoking
        'nausea':'common', #shared between adderall and hallucinogens
        'bad hygeiene':'common',
        'poor hygeine':'common',
        'bad personal grooming':'common',
        'poor personal grooming':'common',
        'stinky':'common',
        'smelly':'common',
        'slurred speech':'common', #shared between alcohol and addy
        'slurred':'common',
        'incoherent speech':'common',





    }

    COURSES = [
        'intro',
        'mathematica',
        'data structures',
        'computer organization',
        'algorithms analysis',
        'hci',
        'c and c',
        'senior seminar',
    ]

    PROFESSORS = [
        'celia',
        'hsing-hau',
        'jeff',
        'justin',
        'kathryn',
    ]


    def __init__(self):
        """Initialize the OxyCSBot.

        The `professor` member variable stores whether the target
        professor has been identified.
        """
        super().__init__(default_state='waiting')
        self.professor = None
        self.course = None               # to store a specific course name

    def get_office_hours(self, professor):
        """Find the office hours of a professor.

        Arguments:
            professor (str): The professor of interest.

        Returns:
            str: The office hours of that professor.
        """
        office_hours = {
            'celia': 'F 12-1:45pm; F 2:45-4:00pm',
            'hsing-hau': 'T 1-2:30pm; Th 10:30am-noon',
            'jeff': 'unknown',
            'justin': 'T 1-2pm; W noon-1pm; F 3-4pm',
            'kathryn': 'MWF 4-5pm',
        }
        return office_hours[professor]

    def get_course_professor(self, course):
            # FIXME
        """ Finds the professor of a course.

        Arguments:
            course (str): The course of interestself.

        Returns:
            str: The professor of that classself.
            If more than one professor for that class, asks which section the student is in
        """

        course_professor = {
            'intro: Hsing-Hua Chen and Kathryn Leonard both teach Fundamentals of Computer Science. Which is your profesor?',
        }

    def get_office(self, professor):
        """Find the office of a professor.

        Arguments:
            professor (str): The professor of interest.

        Returns:
            str: The office of that professor.
        """
        office = {
            'celia': 'Swan 216',
            'hsing-hau': 'Swan 302',
            'jeff': 'Fowler 321',
            'justin': 'Swan B102',
            'kathryn': 'Swan B101',
        }
        return office[professor]

    # "waiting" state functions

    def respond_from_waiting(self, message, tags):
        self.professor = None
        if 'failing' in tags:
            return self.go_to_state('failing')

        if ('intro' in tags) or ('mathematica' in tags) or ('data structures' in tags) or ('computer organization' in tags) or ('algorithms analysis' in tags) or ('hci' in tags):
            return self.go_to_state('specific_class')

        if ('mobile apps' in tags) or ('information theory' in tags) or ('practicum' in tags) or ('junior seminar' in tags):
            return self.go_to_state('spring2018')

        if 'office-hours' in tags:
            for professor in self.PROFESSORS:
                if professor in tags:
                    self.professor = professor
                    return self.go_to_state('specific_faculty')
            return self.go_to_state('unknown_faculty')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.finish('confused')


    # "specific_faculty" state functions

    def on_enter_specific_faculty(self):
        response = '\n'.join([
            f"{self.professor.capitalize()}'s office hours are {self.get_office_hours(self.professor)}",
            'Do you know where their office is?',
        ])
        return response

    def respond_from_specific_faculty(self, message, tags):
        if 'yes' in tags:
            return self.finish('success')
        else:
            return self.finish('location')

    # "failing" state functions
    def on_enter_failing(self):
        return 'Which course are you currently failing?'

    def on_enter_specific_class(self):
        return 'You should get in touch with your professor. Do you know when their office hours are?'

    def on_enter_spring2018(self):
        return ("I'm sorry, I can only help you with courses offered this semester.\n" +
                "Is there anything else I can help you with?")

    # "unknown_faculty" state functions

    def on_enter_unknown_faculty(self):
        return "Who's office hours are you looking for?"

    def respond_from_unknown_faculty(self, message, tags):
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.go_to_state('unrecognized_faculty')

    # "unrecognized_faculty" state functions

    def on_enter_unrecognized_faculty(self):
        return ' '.join([
            "I'm not sure I understand - are you looking for",
            "Celia, Hsing-hau, Jeff, Justin, or Kathryn?",
        ])

    def respond_from_unrecognized_faculty(self, message, tags):
        for professor in self.PROFESSORS:
            if professor in tags:
                self.professor = professor
                return self.go_to_state('specific_faculty')
        return self.finish('fail')

    # "finish" functions

    def finish_confused(self):
        return "Sorry, I'm just a simple bot that understands a few things.\nYou can ask me for advice if you are struggling with computer science!"

    def finish_location(self):
        return f"{self.professor.capitalize()}'s office is in {self.get_office(self.professor)}"

    def finish_success(self):
        return 'Great, let me know if you need anything else!'

    def finish_fail(self):
        return "I've tried my best but I still don't understand. Maybe try asking other students?"

    def finish_thanks(self):
        return "You're welcome!"


if __name__ == '__main__':
    teendrugbot().chat()
