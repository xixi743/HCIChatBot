# HCIChatBot
This chat bot was created for my Human Computer Interaction course. We were tasked with creating a chat bot that attempts a task that requires a human connection. We ended up creating a chat bot that that helps parents figure out what drugs their teens may be experimenting with based off their symptoms and behaviors. After determining the specific drug the teen is using, we give the parent adivce on how to approach the situation. 

This idea came from one of my random thoughts in conversation with my professor and one of my groupmates. We were considering doing a parent chat bot that gave bad advice, but my professor expressed that doing so would be too easy due to the incincerity of the robot. I randomly suggested “What if a parent found drugs under their teen’s bed and our chat bot helped out with that?” Our professor liked the idea! :stuck_out_tongue:

:heavy_exclamation_mark: **This is chatbot is not a medical tool nor does it provide an accurate diagnosis. We are not medical professionals. Please seek professional advice where needed** :heavy_exclamation_mark: 

## How it Works
Once we had our idea, we got down to planning how we would carry it out. We started by creating a flow chart of the actions and dialogue that would occur when chatting with our bot. Then, we started figuring out how we would identify each drug in our chat bot. We decided to implement this by using dictionaries of tags. Our tags consisted of symptoms of drug use, changes in behaviors, drug paraphernalia, and nicknames for different drugs. 

After our dictionaries and dialogue were planned out, we began to code. We started by entering all the tags for our dictionary of drugs and defining the different states our bot could be in. The starting state is “waiting” since the bot is waiting for the user’s input before responding. After that, it will proceed to the “common_symptom” state or the “identified_drug” state depending on if it has identified the drug or not from the user’s first input. If the user mentions a drug name or a symptom/behavior specific to one kind of drug, the chat bot will immediately proceed to giving advice to the user. If the user enters a common symptom or behavior like “coughing”, “smells bad”, or “eating more”, it will enter the “common_symptom” states. It will also enter the “common_symptom” state if it doesn’t recognize the user’s text, as a fail safe. The common symptom states help us narrow down what drug a teen might be using by asking leading questions like “Does your teen have bloodshot eyes often and do they seem to be losing motivation?” If the user answers “yes” then it will enter the “identified_drug” state and give advice about marijuana. If the user doesn’t say “yes”, then it will move on to the next leading question about adderall. It will continue asking leading questions until it passes through all of the drugs in our dictionary. If the user continues to answer “no”, then it will call the “finish_fail()” function which advises the user to speak to a professional.

<p align="center">
  <img src="https://user-images.githubusercontent.com/33335169/57846329-cec84600-7788-11e9-91bf-cbd74cf07997.png"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/33335169/57846546-531ac900-7789-11e9-98a9-c7408c2430ef.png"/>
</p>

## Additional Information
Read the blog post on it at:
https://xixi743.wixsite.com/hale/blog/teen-drug-bot

Demonstration videos:
https://youtu.be/ckoSdJR6SfU
https://youtu.be/0SlZG3_tt4c
