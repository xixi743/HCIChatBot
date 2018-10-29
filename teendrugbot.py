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
            message = input("So, you think your teen is doing drugs? What symptoms are they exhibiting? Any changes in behavior? \n")
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
    """A simple chatbot that directs parents on how to identify what drugs their unruly teens are using."""

    STATES = [
        'waiting',
        'common_symptom',
        'common_symptom_2',
        'common_symptom_3',
        'common_symptom_4',
        'common_symptom_5',
        'common_symptom_6',
        'common_symptom_7',
        'identified_drug'
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
        'grinder':'weed',
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
        'adderall':'addy',
        'talkative': 'addy',
        'excitable': 'addy',
        'aggressive': 'addy',
        'aggression': 'addy',

        # alcohol
        'appetite': 'alcohol',
        'shaking': 'alcohol',
        'grooming': 'alcohol',
        'hygeine': 'alcohol',
        'slurred speech': 'alcohol',
        'bruises': 'alcohol',
        'smell of alcohol': 'alcohol',
        'smells of alcohol':'alcohol',
        'alcohol':'alcohol',
        'gum': 'alcohol',
        'arguments': 'alcohol',
        'accidents': 'alcohol',
        'isolated': 'alcohol',
        'irritability': 'alcohol',
        'outburst': 'alcohol',
        'alcohol': 'alcohol',
        'bottles':'alcohol',
        'bottle':'alcohol',

        # tobacco
        'breath': 'tobacco',
        'bad breath':'tobacco',
        'teeth': 'tobacco',
        'yellow': 'tobacco',
        'fingers': 'tobacco',
        'wheezing': 'tobacco',
        'smoke': 'tobacco',
        'smokey':'tobacco',
        'windows': 'tobacco',
        'burn': 'tobacco',
        'burns': 'tobacco',
        'fire':'tobacco',
        'lighter': 'tobacco',
        'matches': 'tobacco',
        'temper': 'tobacco',
        'tobacco': 'tobacco',

        # cocaine
         'hyper': 'cocaine',
        'pupils': 'cocaine',
        'nose': 'cocaine',
        'snort':'cocaine',
        'behavior': 'cocaine',
        'confidence': 'cocaine',
        'talkative': 'cocaine',
        'powder': 'cocaine',
        'hygeiene': 'cocaine',
        'needle marks': 'cocaine',
        'spoon': 'cocaine',
        'razor': 'cocaine',
        'isolation': 'cocaine',

        # LSD, etc.
         'dry mouth': 'lsd',
        'tingling fingers': 'lsd',
        'weakness': 'lsd',
        'distress': 'lsd',
        'anxiety': 'lsd',
        'anxious': 'lsd',
        'depression': 'lsd',
        'depressed': 'lsd',
        'disoriented': 'lsd',
        'paranoid': 'lsd',
        'convulsions': 'lsd',
        'sweating': 'lsd',
        'chills': 'lsd',
        'vision': 'lsd',
        'hallucinate':'lsd',
        'hallucinogen':'lsd',
        'hallucinating':'lsd',
        'seeing things':'lsd',

        # opioides
        'disoriented': 'opioid',
        'swings': 'opioid',
        'droopy': 'opioid',
        'needles': 'opioid',
        'syringe': 'opioid',
        'spoon': 'opioid',
        'shoelaces': 'opioid',
        'straws': 'opioid',
        'pipe': 'opioid',
        'nose': 'opioid',
        'marks': 'opioid',
        'infection': 'opioid',
        'cuts': 'opioid',
        'scabs': 'opioid',
        'picking': 'opioid',
        'hygiene': 'opioid',
        'motivation': 'opioid',
        'hostile': 'opioid',
        'self esteem': 'opioid',
        'pants': 'opioid',
        'sleeves': 'opioid',

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
        'bad coordination':'common',
        'loss of motivation': 'common', #shared between weed and narcotics
        'no motivation': 'common',
        'lack of motivation': 'common',
        'no enthusiasm': 'common', #shared between weed and narcotics
        'loss of enthusiasm':'common',
        'lack of enthusiasm':'common',
        'paranoia':'common', #shared between weed and hallucinogens
        'paranoid':'common',
        'bag':'common', #cocaine, weed, narcotics, and adderall
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
        'smell':'common',
        'slurred speech':'common', #shared between alcohol and addy
        'slurred':'common',
        'incoherent speech':'common',
        'missing school': 'common',
        'grades': 'common',
        'trouble': 'common',
        'fights': 'common',
        'interest': 'common',
        'sleep': 'common',
        'money': 'money',
        'mood': 'common',
        'weight':'common',
        'eat': 'common,',
        'eating': 'common',
        'dizzy': 'common',
        'nauseous': 'common',
        'heartrate': 'common',
        'heart rate': 'common',
        'pupils': 'common',
        'behavior': 'common',
        'withdrawn': 'common',

        # 'yes' and 'no' tags
        'yes':'yes',
        'yeah':'yes',
        'no':'no',
        'nope':'no',

        'thanks':'thanks',
        'thanks!':'thanks',
        'thank you':'thanks'
    }


    def __init__(self):
        """Initialize the OxyCSBot.

        The `professor` member variable stores whether the target
        professor has been identified.
        """
        super().__init__(default_state='waiting')
        self.drug = 'unknown'

    # "waiting" state functions

    def respond_from_waiting(self, message, tags):
        self.drug = 'unknown'
        if ('alcohol' in tags) or ('cocaine' in tags) or ('weed' in tags) or ('lsd' in tags) or ('tobacco' in tags) or ('addy' in tags):
            if 'alcohol' in tags:
                self.drug = 'alcohol'
            if 'cocaine' in tags:
                self.drug = 'cocaine'
            if 'weed' in tags:
                self.drug = 'weed'
            if 'lsd' in tags:
                self.drug = 'lsd'
            if 'tobacco' in tags:
                self.drug = 'tobacco'
            if 'addy' in tags:
                self.drug = 'addy'
            return self.go_to_state('identified_drug')
        elif 'common' in tags:
            return self.go_to_state('common_symptom')
        elif 'thanks' in tags:
            return self.finish('thanks')
        else:
            return self.go_to_state('common_symptom')

    # "identified_drug" state functions

    def on_enter_identified_drug(self):
        if self.drug == 'weed':
            return 'Sounds like your kid is using marijuana. Is it legal in your state?'
        elif self.drug == 'alcohol':
            return "Seems like your kid is using alcohol. Alcohol is the most popular drug amongst teens. Your child's use " \
                   "of it may be inevitable. \nBecause of this, approach your child with nonjudgmental information on how to " \
                   "drink safely, and let them know you're always around to help. \n\nAny other problems with your kid(s) and drugs?"
        elif self.drug == 'cocaine':
            return "Seems like your kid is using cocaine. \nRIP :(\nCocaine is a highly addictive and dangerous drug. I'd recommend " \
                   "talking to your child (_CALMLY_) and ask how long/how often they've been using. \nIf it's frequent use, rehab" \
                   " is the safest option for your kid. If you're not comfortable with that, drug addiction support groups in your area" \
                   " are also effective. \n\nAny other problems with your kid(s) and drugs?"
        elif self.drug == 'tobacco':
            return "Sounds like your kid is using tobacco!! Interventions are proven to be effective in curbing adolescent use. " \
                   "\n(_CALMLY_) Talk to your child about the harmful long term and short term effects of tobacco. \nAs with anything, " \
                   "reassure your child that you are a resource for them and they can come to you for information, advice, or help." \
                   "\n\nAny other problems with your kid(s) and drugs?"
        elif self.drug == 'addy':
            return "Sounds like your kid is using Adderall recreationally! Approach this issue sensitively. \nWith Adderall abuse, " \
                   "it's important to think about reasons your child may have turned to this substance, and talk to your child about " \
                   "their feelings, stressors, and mental health. \nOnce you know the main reason, help your child address and " \
                   "move past it. If you don't find the reason, make sure you talk to your child about the repercussions of " \
                   "using Adderall without a prescription. \nBe open, be understanding, be kind.\n\nAny other problems with your" \
                   " kid(s) and drugs?"
        elif self.drug == 'lsd':
            return "Sounds like your kid is using hallucinogens. You’re in luck! Or as lucky as you can be with your child using drugs. The FDA has claimed that " \
                   "\nLSD and most other hallucinogens do not make the chemical changes in the brain responsible" \
                   " \nfor the development of cravings like other drugs do, meaning that there is no element of chemically" \
                   " \ndependent drug seeking behavior. Although there is no chemical addiction, your kid could still have " \
                   "\na general addiction to the effects of hallucinogens. If your kid is addicted, they’d be taking " \
                   "\nhallucinogens with other substances to heighten the experience of hallucinogens, spending " \
                   "\nsubstantial amounts of time or money on obtaining or using hallucinogens, and neglecting " \
                   "\nresponsibilities or hobbies as a result of continued hallucinogen use. " \
                   "\n\nIs your child doing any of those things?"
        return self.finish_fail()

    def respond_from_identified_drug(self, message, tags):
        if self.drug == 'weed':
            if 'yes' in tags:
                return 'Everyone smokes it now. Warn your kid of the repercussions and move on.\n\nFor more help and advice, leave this instance of the ' \
                       'teendrugbot and come back!'
            else:
                return "As far as drugs go, that ain't bad! Confiscate it for yourself.\n\nFor more help and advice, leave this instance of the " \
                       "teendrugbot and come back!"
        elif self.drug == 'lsd':
            if 'yes' in tags:
                return "Gosh diddly darn. That’s pretty serious! Hallucinogens require larger amounts over time to " \
                       "\nexperience the desired effects, which means it’s really easy to overdose with consistent use, " \
                       "\nand bad trips that put your kid in danger are more frequent. Talking to your kid about how " \
                       "\ndangerous hallucinogens can be is the best first step. Then from there, you can either use a " \
                       "\nbrief intervention technique, or community reinforcement and family training (CRAFT), both of " \
                       "\nwhich are backed by a bunch of research. Brief interventions are essentially short counseling " \
                       "\nsessions—lasting anywhere from 5-30 minutes—that are administered by trained healthcare " \
                       "\nproviders. CRAFT, on the other hand, is a way to increase compliance of your kid in substance " \
                       "\nabuse treatment by properly engaging family and community members. People who comprise " \
                       "\nyour kid’s support system are trained in ways that strengthen this system and maximize the " \
                       "\nindividual’s chances of maintaining sobriety.\n\nFor more help and advice, leave this instance of the " \
                       "teendrugbot and come back!"
            else:
                return "Alrighty then! Helping your kid is pretty straightforward. " \
                       "\nIt’s really about talking to your kid in an open way where you’re really trying to hear " \
                       "\nthem. Then, once you’ve addressed the issue yourself, providing group and individual therapy " \
                       "\nare effective ways to address the reasons behind the substance use and helping your to develop" \
                       " \nboth better coping skills and techniques to prevent relapse.\n\nFor more help and advice, leave this instance of the " \
                       "teendrugbot and come back!"
        else:
            if 'yes' in tags:
                return "I'm happy to help! Please leave this instance of the teendrugbot and come back with your next problem!"
            elif 'thanks' in tags:
                return self.finish_thanks()
            else:
                return self.finish_success()

    # "common_symptom" state functions

    def on_enter_common_symptom(self):
        return "Sorry, I'll need a bit more information to determine what kind of drug your teen is experimenting with. \n" \
               "Does your teen have bloodshoot eyes often and do they seem to be losing motivation?"

    def respond_from_common_symptom(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "weed"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_2')

    def on_enter_common_symptom_2(self):
        return "Is your teen being overly talkative and unusually excitable?"

    def respond_from_common_symptom_2(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "addy"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_3')

    def on_enter_common_symptom_3(self):
        return "Is your teen getting into fights and unable to do complex tasks?"

    def respond_from_common_symptom_3(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "alcohol"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_4')

    def on_enter_common_symptom_4(self):
        return "Have you noticed your teen coughing/wheezing a lot or if they have stained/yellow fingers?"

    def respond_from_common_symptom_4(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "tobacco"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_5')

    def on_enter_common_symptom_5(self):
        return "Has your teen been getting frequent nose bleeds or often have a runny nose?"

    def respond_from_common_symptom_5(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "cocaine"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_6')

    def on_enter_common_symptom_6(self):
        return "Has your teen been hallucinating and seeing things that aren't there?"

    def respond_from_common_symptom_6(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "lsd"
            return self.go_to_state('identified_drug')
        else:
            return self.go_to_state('common_symptom_7')

    def on_enter_common_symptom_7(self):
        return "Have you noticed any injection marks on your teen?"

    def respond_from_common_symptom_7(self, message, tags):
        if ("yes" in tags) or ('yep' in tags) or ("ye" in tags):
            self.drug = "opioid"
            return self.go_to_state('identified_drug')
        else:
            return self.finish_fail()

    # "finish" functions

    def finish_success(self):
        return 'Great, let me know if you need anything else!'

    def finish_fail(self):
        return "I've tried my best but I still don't understand. Maybe try asking a human health professional?"

    def finish_thanks(self):
        return "You're welcome!"


if __name__ == '__main__':
    teendrugbot().chat()
