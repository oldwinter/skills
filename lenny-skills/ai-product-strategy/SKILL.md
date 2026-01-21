# AI Product Strategy

**Category:** AI & Technology

**Source:** https://refoundai.com/lenny-skills/s/ai-product-strategy

---

AI Product Strategy | Refound AI

Lenny Skills Database     SKILLS  PLAYBOOKS  GUESTS  ABOUT               SKILLS  PLAYBOOKS  GUESTS  ABOUT                     AI & Technology   94 guests | 179 insights

AI Product Strategy  AI product strategy is about building for a moving target. The underlying technology changes faster than your planning cycles, so you need to design products that get better as models improve, build feedback loops that compound your advantage, and avoid the trap of solving current limitations that will disappear in six months.

Download Claude Skill

Read Guide

The Guide  5 key steps synthesized from 94 experts.

1 Build for the model that's coming, not the one you have  If you're designing around today's limitations, you'll ship an obsolete product. The models are improving on a predictable curve. Build features that would be transformative with better reasoning, faster inference, or lower costs—even if they don't fully work today. The models will catch up.

Featured guest perspectives

"Don't build for today, build for six months from now, build for a year from now. And the things that aren't quite working that are working 20% of the time, will start working 100% of the time."

— Benjamin Mann    "Our general mindset is in two months, there's going to be a better model and it's going to blow away whatever the current set of limitations are... If you're building and the product is right on the edge of the capabilities of the models, keep going because you're doing something right."

— Kevin Weil    "Too many people are building things to make up and compensate for the LLMs that all that work is going to go away. So it's okay to do it to understand that it's going to go away, but that can't be your differentiator."

— Tamar Yehoshua        2 Design for the squishy middle, not perfect accuracy  LLMs will never be 100% accurate. If your product design assumes perfect outputs, you're building for a fantasy. The best AI products account for uncertainty, make errors recoverable, and are transparent about limitations. The question isn't 'how do we make it perfect?' but 'how do we make it useful despite imperfection?'

Featured guest perspectives

"Even if you get it down to 99% of the time it's fine. If it punches the user in the face, that's not a viable product. And so how do you design your products assuming that this thing will be squishy and not fully accurate?"

— Alex Komoroske    "The promise of the UI has to match the quality of the underlying data... one of the failings of the various LMs right now is they all appear supremely confident even when they're completely hallucinating."

— Noah Weiss        3 Create feedback loops that make your product smarter  The sustainable moat in AI isn't the model—it's the data flywheel. Every user interaction should make your product better. Capture feedback, log edge cases, use production data to improve prompts and fine-tuning. The companies that win are the ones building systems that learn, not static wrappers.

Featured guest perspectives

"When you're building AI products, it's a constant stream of user feedback... the whole idea is to capture users' feedback so the next iteration of the model, the prompt, the fine-tuning, the examples, the RAG is better."

— Guillermo Rauch    "It's not about being the first company to have an agent among your competitors. It's about have you built the right flywheels in place so that you can improve over time."

— Aishwarya Naresh Reganti + Kiriti Badam        4 Master evals—they're your new product requirements  In AI products, evaluations are the PRD. You can't improve what you can't measure. Build systematic ways to assess whether your AI is doing what users need. Write evals before you write prompts. Use domain experts to judge quality, not just automated metrics that can be gamed.

Featured guest perspectives

"To build great AI products, you need to be really good at building evals. It's the highest ROI activity you can engage in... it really is, at its core, data analytics on your LLM application."

— Hamel Husain & Shreya Shankar    "I started writing evals before I knew what an eval was because I was just outlining very clearly specified ideal behavior for various use cases... it might be the lingua franca of how to communicate what the product should be doing."

— Nick Turley        5 Start with the problem, not the technology  The trap is building AI because you can, not because you should. Work backwards from a real user problem. Would this be valuable if you had to fake it? If the answer is no, the AI won't save it. The best AI products feel like magic because they solve genuine pain, not because they use sophisticated technology.

Featured guest perspectives

"What is that problem that we're trying to solve and how can we leverage AI better to help solve the problem versus what do we do with AI? So it's really working backwards from the customer problem."

— Inbal S    "Where companies fail is that they're doing AI for AI's sake. They have a ton of projects that they're kicking off at the same time without a blueprint to understand how it actually worked."

— Asha Sharma

✗ Common Mistakes

Building scaffolding for current model limitations that will disappear with the next releaseTreating AI as a feature to bolt on rather than a foundation to build fromChasing benchmarks instead of solving real user problemsSkipping evals because 'vibes' seem good enoughAssuming you need to build your own models when fine-tuning or prompting would suffice     ✓ Signs You're Doing It Well

Your product gets measurably better with each model upgradeYou have systematic evals that correlate with user satisfactionUsers give you feedback you can actually act on to improve the AIYou can articulate specifically what the AI does better than alternatives—human or softwareYou're shipping features that feel slightly ahead of what's reliable, betting on the improvement curve

All Guest Perspectives

Deep dive into what all 94 guests shared about ai product strategy.

Alex Hardimen 1 quote

Listen to episode →

"We're training algorithms on specific data sets, like editorial important scores that actually come from our journalists. What that allows us to do is actually scale editorial judgment to a large group of readers. Those algorithms... they're trained on editorial signal and then they can still work towards driving towards outcomes like reach, engagement, conversion, et cetera."  Tactical:  Train algorithms on proprietary 'expert' data sets (e.g., editorial scores)Use AI to scale human judgment to a larger audienceBalance expert signals with traditional engagement outcomes

View all skills from Alex Hardimen →

Adriel Frederick 2 quotes

Listen to episode →

"When you are working on algorithmic heavy products, your job is figuring out what the algorithm should be responsible for, what people are responsible for, and the framework for making decisions."  Tactical:  Identify which decisions require long-term strategic intent that algorithms cannot yet grasp.Create a framework that specifies the responsibilities of the machine versus the human operator.    "It's more about giving people the information that they can use for decisions that they alone are good at and giving machines the power to amplify a person's intent... I think about it as designing an interface and make it an extension of yourself rather than a black box."  Tactical:  Design interfaces that provide humans with the necessary context to make strategic choices.Use ML to optimize for specific objectives while allowing humans to set the strategic constraints.

View all skills from Adriel Frederick →

Albert Cheng 1 quote

Listen to episode →

"Behind the scenes, we're running chess engines to basically spit out evaluations for every move that you make. And then we translate that and make that approachable to the user using their native language and plain approachable style... that part is LLMs."  Tactical:  Use LLMs to translate complex technical data (like engine evaluations) into natural, encouraging language for the user.

View all skills from Albert Cheng →

Alexander Embiricos 3 quotes

Listen to episode →

"One of our major goals with Codex is to get to proactivity. If we're going to build a super system, has to be able to do things. One of the learnings over the past year is that for models to do stuff, they're much more effective when they can use a computer. It turns out the best way for models to use computers is simply to write code. And so we're kind of getting to this idea where if you want to build any agent, maybe you should be building a coding agent."  Tactical:  Prioritize coding capabilities as the core competency for any functional AI agentFocus on 'proactivity' where the agent chimes in or takes action without a direct prompt    "I actually think Chat is a very good interface when you don't know what you're supposed to use it for... you start using it even outside of work to just help you. You become very comfortable with the idea of being accelerated with AI. So then you get to work and you just can naturally just, 'Yeah, I'm just going to ask it for this and I don't need to know about all the connectors or all the different features.'"  Tactical:  Use Chat as the entry point for discovery and general assistanceSurface specialized GUIs only when the user needs to go deep into a functional domain like coding    "I think that the current limiting factor, I mean, there's many, but I think a current underappreciated limiting factor is literally human typing speed or human multitasking speed on writing prompts... we need to unblock those productivity loops from humans having to prompt and humans having to manually validate all the work."  Tactical:  Build systems that allow agents to be 'default useful' without constant promptingDevelop automated validation loops so humans don't have to manually review every AI action

View all skills from Alexander Embiricos →

Aishwarya Naresh Reganti + Kiriti Badam 4 quotes

Listen to episode →

"Most people tend to ignore the non-determinism. You don't know how the user might behave with your product, and you also don't know how the LLM might respond to that. The second difference is the agency control trade-off. Every time you hand over decision-making capabilities to agentic systems, you're kind of relinquishing some amount of control on your end."  Tactical:  Account for non-deterministic user behavior in natural language interfaces.Balance the level of agency granted to an agent against the amount of control the user retains.    "So we recommend building step-by-step. When you start small, it forces you to think about what is the problem that I'm going to solve. In all this advancements of the AI, one easy, slippery slope is to keep thinking about complexities of the solution and forget the problem that you're trying to solve."  Tactical:  Start with minimal impact use cases to gain a grip on current capabilities.Gradually increase agency as confidence in the system's reliability grows.    "It's not about being the first company to have an agent among your competitors. It's about have you built the right flywheels in place so that you can improve over time."  Tactical:  Focus on building a pipeline that learns and improves over time rather than a 'one-click' solution.Log human actions in early versions to create a data flywheel for system improvement.    "I used to work with the CEO of now Rackspace, Gagan. So he would have this block every day in the morning, which would say catching up with AI 4:00 to 6:00 AM... I think leaders have to get back to being hands-on. And that's not because they have to be implementing these things, but more of rebuilding their intuitions because you must be comfortable with the fact that your intuitions might not be right."  Tactical:  Block dedicated time daily to stay updated on AI developments.Be willing to challenge and relearn long-held product intuitions in the context of AI.

View all skills from Aishwarya Naresh Reganti + Kiriti Badam →

Alex Komoroske 2 quotes

Listen to episode →

"I think LLMs are truly a disruptive technology. In fact, I would argue that what we're seeing in the industry is us trying to use mature playbooks from the end stage of the last tech era in one that doesn't really fit yet. To me, LLMs are magical duct tape. They're formed principally by the distilled intuition of all of society into a thing that operates between, a cost structure between human and plain old computing."  Tactical:  Recognize that LLMs make writing 'good enough' software significantly cheaper but increase marginal inference costs.Avoid consumer startup models based solely on advertising, as ad revenue may not clear inference costs.    "I see all these places where people will build products and they'll say 80% of the time, 90% percent of the time, it's great. 5% of the time it punches the user in the face... even if you get it down to 99% of the time, it's fine. If it punches in the face, that's not a viable product. And so how do you design your products assuming that this thing will be squishy and not fully accurate and fully work?"  Tactical:  Design product UX to handle cases where the AI might be inaccurate or fail.Focus on building what is possible now that 'magical duct tape' (LLMs) exists, rather than just trying to make the AI 100% autonomous.

View all skills from Alex Komoroske →

Amjad Masad 2 quotes

Listen to episode →

"I actually wrote about it back in '22. I said it's going to be society of models, like products will be made of a lot of different models, and it's quite a heavy engineering project."  Tactical:  Architect systems to leverage multiple foundation models based on their specific strengths (e.g., reasoning vs. speed).    "I could imagine whatever, five years from now, someone running a billion dollar company with zero employees where it's like the support is handled by AI, the development is handled by AI, and you're just building and creating this thing that people are finding valuable."  Tactical:  Evaluate business models that can scale to high revenue with minimal headcount by leveraging autonomous agents.

View all skills from Amjad Masad →

Anton Osika 2 quotes

Listen to episode →

"The reason why we're doing Lovable is that I don't know about your mom, but my mom doesn't write code... we are building for this 99% of the population who don't write code."  Tactical:  Target the '99%' who lack specialized technical skillsFocus on natural language interfaces to lower the barrier to entry    "The frontier of where this is a problem is very rapidly receding back. So what we did was we identified the most important areas, so specifically adding login, creating data persistence, adding payment with Stripe. Those are the things that we made sure it doesn't get stuck on."  Tactical:  Identify common failure points in AI generation (e.g., auth, payments)Tune the system quantitatively to address these specific bottlenecks

View all skills from Anton Osika →

Aparna Chennapragada 1 quote

Listen to episode →

"When I think about agents, I think about these three things. One is an increasing level of autonomy and kind of independence that you can delegate higher and higher order tasks. Second, I think of as complexity. It's not a one-shot, 'Hey, create this image or do this thing or summarize the document,' it's build me this prototype that expresses my idea of, say, an augmented reality app. And then the third one I think of is it's a much more natural interaction."  Tactical:  Design for delegation of high-level goals rather than just fine-motor assistanceFocus on complex, multi-step workflows over simple one-shot promptsIncorporate asynchronous capabilities so the agent works while the user is away

View all skills from Aparna Chennapragada →

Asha Sharma 3 quotes

Listen to episode →

"all of a sudden these are these living organisms that just get better with the more interactions that happen. I think this is the new IP of every single company products that think and live and learn."  Tactical:  Focus on the 'metabolism' of the product team to ingest data and digest rewards modelsTune models toward specific outcomes like price, performance, or quality    "I think that where companies fail is that they're doing AI for AI's sake. They have a ton of projects that they're kicking off at the same time without a blueprint to understand how it actually worked and what their Stack looks like and they aren't treating it like a real investment, and so they don't have the measurement and the observability and the evals all set up."  Tactical:  Establish clear measurement, observability, and evaluation frameworks (evals) before scalingMap out existing processes and apply AI to specific pain points like customer support or fraud reduction    "I feel like you have to actually build for the slope instead of the snapshot of where you are."  Tactical:  Build flexible architectures that allow for swapping models or tools as they improveAnticipate exponential demand for productivity as the marginal cost of output approaches zero

View all skills from Asha Sharma →

Benjamin Mann 3 quotes

Listen to episode →

"I think progress has actually been accelerating where if you look at the cadence of model releases, it used to be once a year and now with the improvements in our post-training techniques, we're seeing releases every month or three months, and so I would say progress is actually accelerating in many ways, but there's this weird time compression effect."  Tactical:  Monitor the cadence of model releases rather than just the magnitude of single leaps to gauge industry progressAccount for 'time dilation' in AI development where rapid iterations can mask the underlying exponential growth    "I think my favorite role in that time has been when I started the labs team about a year ago, whose fundamental goal was to do transfer from research to end user products and experiences. Because fundamentally I think the way that Anthropic can differentiate itself and really win is to be on the cutting edge."  Tactical:  Create a specialized team to handle the 'transfer' from research breakthroughs to product featuresFocus on 'computer use' and credential management as a high-trust, high-differentiation product area    "I guess concretely we think about skating to where the puck is going and what that looks like is really understand the exponential... don't build for today, build for six months from now, build for a year from now. And the things that aren't quite working that are working 20% of the time, will start working 100% of the time."  Tactical:  Build for the model capabilities expected in 6-12 months to avoid shipping obsolete productsInvest in features that have low reliability today (e.g., 20% success) if they are on an exponential improvement curve

View all skills from Benjamin Mann →

Ben Horowitz 2 quotes

Listen to episode →

"I think the application layer is going to be very, very interesting... Chat GPT, like it or not, it's got a real moat... the applications are both more complex and kind of stickier than people thought they were originally. The thing that people got very wrong is this whole thin wrapper around GPT, that's really wrong."  Tactical:  Avoid building 'thin wrappers'; focus on deep domain integrationLook for opportunities where software previously couldn't solve the problem    "Everything that we couldn't solve with software we can solve now, almost. So it's a really big world."  Tactical:  Identify 'fat-tail' human behaviors or rare edge cases that traditional code couldn't handle

View all skills from Ben Horowitz →

Brian Balfour 2 quotes

Listen to episode →

"My prediction, the new distribution platform will be ChatGPT... I think the bigger thing will be whatever they do with launching a third-party platform on top of ChatGPT, there's a bunch of signals that they're about to launch that."  Tactical:  Monitor for the emergence of third-party agent platforms as new distribution channels.Evaluate AI platforms based on retention and depth of engagement rather than just monthly active users (MAU).    "My hypothesis... is that the moat is about context and memory. These models by themselves, if you compare them side by side, they generate the same result, and so the actual difference-maker is which one has more of your context, because it's the context plus the model that produces the best output."  Tactical:  Invest in 'context connectors' that allow your product to store and recall user-specific data.Focus on creating a flywheel where more usage leads to better personalized context and superior outputs.

View all skills from Brian Balfour →

Cam Adams 1 quote

Listen to episode →

"We approach AI inside the product through three pillars. First of these is that we need to build some of our own AI tech... Second pillar is just finding the world's best AI people to partner with... And for us, the third pillar is our app ecosystem."  Tactical:  Build proprietary AI only where you have a data advantage or it is critical to the core businessPartner with best-in-class providers for commodity AI needs like LLMsCreate an app ecosystem to allow third-party AI developers to reach your user base

View all skills from Cam Adams →

Bret Taylor 2 quotes

Listen to episode →

"I think there's three segments of the AI market... frontier model market... tooling... applied AI market. I think this will play out for companies who build agents. I think agent is the new app."  Tactical:  Focus on 'Applied AI' where the agent is the primary product form factorBuild agents that accomplish jobs autonomously rather than just increasing individual productivity    "The whole market is going to go towards agents. I think the whole market is going to go towards outcomes-based pricing. It's just so obviously the correct way to build and sell software."  Tactical:  Orient product strategy around autonomous task completion rather than just human-in-the-loop tools

View all skills from Bret Taylor →

Chip Huyen 3 quotes

Listen to episode →

"What actually improves AI apps, talking to users, building more reliable platforms, preparing better data, optimizing end-to-end workflows, writing better prompts."  Tactical:  Prioritize talking to users over staying up to date with every AI news cycleFocus on writing better prompts and optimizing end-to-end workflowsAvoid over-committing to new, untested technologies that are hard to switch out later    "I do ask people to ask their managers, 'Would you rather give everyone on the team very expensive coding agent subscriptions or you get an extra head count?' Almost every one, the managers will say head count."  Tactical:  Use the 'headcount vs. AI subscription' question to gauge the perceived value of AI tools within a teamFocus on identifying use cases with clear, measurable outcomes (like conversion rates in sales bots) to drive adoption    "When it comes to, think about voice, it's an entirely different beast... we need to think about latency because I think multiple steps... And there's a question, what does it make you sound natural?"  Tactical:  Solve for 'forced interruption' to make voice bots feel naturalOptimize the multi-hop latency (STT to LLM to TTS) for real-time interaction

View all skills from Chip Huyen →

Chandra Janakiraman 1 quote

Listen to episode →

"There are two ways to get AI to assist you in the strategy formulation process. The first is to support the preparation phase in terms of research... The second one is in this idea called generating mock strategies."  Tactical:  Use AI to analyze themes across a vast library of competitor release notesGenerate 'mock strategies' with LLMs to identify comprehensive investment areas before human down-selection

View all skills from Chandra Janakiraman →

Christopher Miller 1 quote

Listen to episode →

"I get to help lead HubSpot in terms of how we should be thinking about building the foundational technology to create AI-powered experiences and then also lead the strategy of how we leverage those experiences to help that B2B business builder be way more successful using our platform than they might've been in years past."  Tactical:  Focus on building foundational technology that can power multiple AI experiencesLeverage AI to help users achieve outcomes more successfully than traditional software methods

View all skills from Christopher Miller →

Claire Vo 1 quote

Listen to episode →

"I hold myself to the bar as a technology leader, I need to be leading the league on understanding what this can disrupt, using these tools to make a better team, and actually shifting the size and shape of my organization in response to the technology around us."  Tactical:  Automate a role for a week before opening a new job descriptionShift focus from 'communication' (trading info) to 'influence' (getting buy-in)Study non-deterministic products to understand how they differ from traditional software

View all skills from Claire Vo →

David Placek 1 quote

Listen to episode →

"Engineers come to us wanting more sophisticated names where they are likely to end up with another Codium or an Anduril or an Anthropic... we think what you're doing needs to be much more tangible, and something that people can grab onto, and much more natural as opposed to a Codium."  Tactical:  Move away from abstract, technical-sounding names in AIUse metaphors and natural concepts (e.g., Windsurf) to make AI feel more accessible

View all skills from David Placek →

Dan Shipper 2 quotes

Listen to episode →

"There are these things that were historically really expensive that only rich people or big companies could buy... what AI does is it allows you to be like, oh, I could just use cloud for that... And then if it does, we will unbundle it into its own separate thing that becomes an app."  Tactical:  Test product ideas first using general-purpose chatbots (ChatGPT/Claude) to see if the workflow is valuableMeasure product success by internal adoption within your own team before launching publicly    "I think the number one predictor is, 'Does the CEO use ChatGPT?'... If the CEO is in it all the time, being like, 'This is the coolest thing,' everybody else is going to start doing it. If the CEO is like, 'I don't know, this is for someone else,' no one else is going to be able to lead that charge."  Tactical:  CEOs should explicitly mention in memos when they have used AI to draft the contentLead from the front by setting reasonable expectations based on personal usage experience

View all skills from Dan Shipper →

Dalton Caldwell 1 quote

Listen to episode →

"Small fine tune models as an alternative to gigantic generic ones... we'll probably be able to create better and better glue so all sorts of software systems can talk to each other. And so again, very broad idea. But yeah, I think we'll see a lot of very successful companies where that's the kernel of the idea they start with."  Tactical:  Explore small, fine-tuned models for specific vertical use casesIdentify brittle enterprise 'glue' that can be replaced or improved with LLMs

View all skills from Dalton Caldwell →

Dr. Fei Fei Li 4 quotes

Listen to episode →

"That combination of the trio technology, big data, neural network, and GPU was kind of the golden recipe for modern AI. And then fast-forward, the public moment of AI, which is the ChatGPT moment, if you look at the ingredients of what brought ChatGPT to the world technically still use these three ingredients."  Tactical:  Focus on the 'trio' of technology: big data, neural networks, and compute (GPUs).Recognize that scaling existing architectures is necessary but insufficient for future breakthroughs.    "I think scaling loss of more data, more GPUs, and bigger current model architecture is there's still a lot to be done there, but I absolutely think we need to innovate more. There's not a single deeply scientific discipline in human history that has arrived at a place that says we're done, we're done innovating and AI is one of the, if not the youngest discipline in human civilization."  Tactical:  Look beyond current transformer architectures for innovations in abstraction and creativity.Identify 'North Star' problems like object recognition or spatial intelligence to drive model development.    "A simple way to understand a world model is that this model can allow anyone to create any worlds in their mind's eye by prompting whether it's an image or a sentence. And also be able to interact in this world whether you are browsing and walking or picking objects up or changing things as well as to reason within this world."  Tactical:  Develop models that allow for interaction and reasoning within a 3D space rather than just 2D output.Use world models as a foundation for embodied AI (robotics) and spatial intelligence.    "It turns out simpler model with a ton of data always win at the end of the day instead of the more complex model with less data... why can't bitter lesson work in robotics alone? ...you hope to get actions out of robots, but your training data lacks actions in 3D worlds... we have to find different ways to fit a, what do they call, a square in a round hole, that what we have is tons of web videos."  Tactical:  Supplement web video data with teleoperation or synthetic data to train robotic models.Recognize that robotics requires physical bodies and supply chains, making the productization journey longer than software-only AI.

View all skills from Dr. Fei Fei Li →

Dhanji R. Prasanna 2 quotes

Listen to episode →

"Our number one priority is through automate Block, which means getting AI and getting AI forms of automation through our entire company. ... we find engineering teams that are very, very AI forward that are using Goose every day are reporting about eight to 10 hours saved per week, and this is self-reported."  Tactical:  Measure AI impact through 'manual hours saved' across all departments, not just engineeringUse data scientists to validate self-reported productivity gains with throughput metrics like PR volume    "The truth is the value is changing every day. And so you need to be adaptable and look at what the value is today and plan for what the value will be tomorrow and then slowly expand to the areas where it's most efficacious."  Tactical:  Identify areas where AI currently outperforms humans (e.g., simple tool building) vs. where it underperforms (e.g., complex architecture)Ride the wave of model improvements rather than waiting for a 'final' version of the technology

View all skills from Dhanji R. Prasanna →

Drew Houston 1 quote

Listen to episode →

"Dash connects to all your different apps. It gives you universal search. Then obviously after ChatGPT, not only can you do conventional search, but you can ask questions in natural language, and answer a lot of the questions that ChatGPT can't because it's not connected to your stuff."  Tactical:  Build connector platforms to index the 'known universe' of SaaS apps to provide personalized AI answers.Focus on universal search and natural language queries as a way to organize a user's working life.

View all skills from Drew Houston →

Dharmesh Shah 1 quote

Listen to episode →

"we're going from what was an imperative model... to what engineers would call a declarative model. A declarative model is you describe the outcome you want, not the steps to get there"  Tactical:  Identify use cases where the 'translation layer' between a user's thought and the software's interface can be eliminated.Build products that allow users to express intent rather than execute steps.

View all skills from Dharmesh Shah →

Dylan Field 2 quotes

Listen to episode →

"I was looking online on social media and I think people are already zeroing in the right conversation, which is, okay, in a world of more software being created by AI, what does that mean and the impact on craft and the impact on quality and the need to have more unique design and how design is a differentiator."  Tactical:  Evaluate how AI-generated features impact the overall quality and 'soul' of the productIdentify areas where AI can handle 'obvious' tasks to allow humans to focus on unique differentiation    "PMs are no longer saying to the designer, 'Hey, can you draw this thing out for me?' That frees up designer time to go explore more deeply the stuff they need to go into and it allows anyone to add to that first conversation of, where should we go?"  Tactical:  Use AI to democratize the prototyping process across non-design functionsFocus AI strategy on shortening the path from idea to working prototype

View all skills from Dylan Field →

Edwin Chen 4 quotes

Listen to episode →

"I'm worried that instead of building AI that will actually advance us as a species, curing cancer, solving poverty, understand the universe, we are optimizing for AI slop instead. But we're optimizing your models for the types of people who buy tabloids at a grocery store. We're basically teaching our models to chase dopamine instead of truth."  Tactical:  Avoid optimizing models solely for user engagement or 'dopamine' hitsFocus on 'truth' and high-utility outcomes rather than superficial performance    "I don't trust the benchmarks at all... the benchmarks themselves are often honestly just wrong. They have wrong answers... these benchmarks at the end of the day, they often have well-defined objective answers that make them very easy for models to hill-climb on in a way that's very different from the messiness and ambiguity of the real world."  Tactical:  Be skeptical of model performance on academic benchmarksPrioritize testing models against messy, ambiguous real-world tasks rather than objective-answer benchmarks    "The way we really care about measuring model progress is by running all these human evaluations... because or searchers or annotators, they are experts at the top of their fields, and they are not just giving your responses, they're actually working through the responses deeply themselves... they're going to evaluate the models in a very deep way, so they're going to pay attention to accuracy and instruction following, all these things that casual users don't"  Tactical:  Use expert human annotators to fact-check and deeply evaluate model outputsLook beyond 'vibes' and flashy responses to measure accuracy and instruction following    "I've realized that the values that the companies have will shape the model... Do you want a model that says, 'You're absolutely right. There are definitely 20 more ways to improve this email,' and it continues for 50 more iterations or do you want a model that's optimizing for your time and productivity and just says, 'No. You need to stop. Your email's great. Just send it and move on'?"  Tactical:  Define the specific 'personality' and value system you want your AI product to embodyDecide whether to optimize for user engagement (time spent) or user productivity (time saved)

View all skills from Edwin Chen →

Eoghan McCabe 3 quotes

Listen to episode →

"You don't have a choice. AI is going to disrupt in the most aggressive violent ways. If you're not in it, you're about to get kicked out of all of it."  Tactical:  Acknowledge that AI will disrupt almost all software categories.Move aggressively to be part of the disruption rather than fighting it.    "We were only six weeks into the launch of GPT 3.5 when we actually had a beta version of Fin. I got a text from Des, my co-founder, a week or so after the launch of GPT 3.5 and he said, 'The AI team have something interesting and they actually think we could make a product out of this.'"  Tactical:  Empower existing AI/ML teams to experiment immediately with new models.Aim for a working prototype within weeks of a major model release.    "I jumped hard on AI and announced that we were going to spend nearly $100 million of our own cash on that. We allocated a lot of capital, but I also restarted the culture."  Tactical:  Allocate substantial budget specifically for AI development.Align company culture with the demands of the AI era (speed, resilience).

View all skills from Eoghan McCabe →

Eric Ries 1 quote

Listen to episode →

"AI is a management technology. The thing it does is manage intelligence and other intelligences... It will really change management a lot because it changes the individual span of control quite a lot."  Tactical:  Use AI for summarization of organizational activityDesign agents with clear procurement policiesPick actions that make ethical sense in a wide variety of future scenarios

View all skills from Eric Ries →

Ethan Smith 2 quotes

Listen to episode →

"Answer Engine Optimization is how do I show up in LLMs as an answer?"  Tactical:  Focus on getting mentioned as many times as possible across various citations rather than just ranking for a single link.Optimize for the 'long tail' of conversational questions which are more prevalent in chat than traditional search.    "The LLM is summarizing many citations and so you need to get mentioned as many times as possible. Usually when you ask something like, 'What's the best tool for X?' The first answer will be mentioned the most in the citations."  Tactical:  Identify the specific citations (websites, videos, threads) the LLM is pulling from.Increase brand mentions in those specific high-authority citations to move up the LLM's internal ranking.

View all skills from Ethan Smith →

Eric Simons 2 quotes

Listen to episode →

"Software is deterministic. When you write code and you hit run, it either runs or it doesn't... It makes technical sense why, of anything, LLMs are going to get insanely better at writing code than probably most other types of applications for LLMs."  Tactical:  Focus AI efforts on tasks that have deterministic outcomes (like code execution)Use automated environments to generate high-quality training data through reinforcement learning    "PMs, they're going to be 'writing code', quote, unquote, instead of just writing a JIRA ticket and waiting for a developer to do it... The winners, at least, their org charts are going to completely change, and how they approach building products and shipping products."  Tactical:  Prepare for an org chart where PMs and designers have direct 'fingertip' access to the codebase via AIShift engineering resources away from 'cookie-cutter' UI work toward intellectually challenging tasks

View all skills from Eric Simons →

Geoffrey Moore 1 quote

Listen to episode →

"From a customer's point of view, there's AI in the early market, there's AI in the bowling alley, there's AI in the chasm, there's AI in the tornado, and there's AI on Main Street."  Tactical:  Identify if your AI feature is a 'Main Street' productivity add-on (like Copilot) or a 'Bowling Alley' specialized solution (like AI tutoring).For specialized AI, focus on high-productivity returns with modest risk.

View all skills from Geoffrey Moore →

Gaurav Misra 1 quote

Listen to episode →

"Our goal specifically for video is not to build professional tools... We're building for the person who could not have created video before."  Tactical:  Identify 'skill gaps' or 'time gaps' that AI can bridge for users who lack professional tools.Focus on specific AI niches (like talking videos) rather than general-purpose generation to solve practical problems.Differentiate between 'documentation' video (real) and 'storytelling' video (AI-enhanced) to guide safety and product focus.

View all skills from Gaurav Misra →

Hamel Husain & Shreya Shankar 3 quotes

Listen to episode →

"To build great AI products, you need to be really good at building evals. It's the highest ROI activity you can engage in."  Tactical:  Focus on building evals as a core competencyPrioritize systematic measurement over vibe checks    "Evals is a way to systematically measure and improve an AI application, and it really doesn't have to be scary or unapproachable at all. It really is, at its core, data analytics on your LLM application"  Tactical:  Treat evals as a systematic measurement frameworkUse data analytics principles to iterate on LLM applications    "You can appoint one person whose taste that you trust. It should be the person with domain expertise. Oftentimes, it is the product manager."  Tactical:  Appoint a single domain expert to lead open codingEnsure the person with the best 'taste' for the product defines the quality bar

View all skills from Hamel Husain & Shreya Shankar →

Grant Lee 1 quote

Listen to episode →

"It's not just one model. It's maybe 20 plus models powering all different parts of the product, and then you're thinking about the orchestration that's required and you're thinking about, obviously if you're experimenting constantly being able to test across the newest models versus models that have been around that are cheaper, you're doing a lot to really... Your job is to, again, align value, maximize the value you're delivering to the end user in a way that's sustainable for you as a business."  Tactical:  Own the end-to-end workflow rather than just providing a single AI feature.Use different models for different tasks (e.g., one for outlining, one for visual layout, one for image generation).Constantly experiment with new models to balance performance with inference costs.

View all skills from Grant Lee →

Hamilton Helmer 1 quote

Listen to episode →

"Will AI models develop so that they learn in a way that for one user's interaction helps another user's interaction? That would be a powerful network economy. Or if it learns, if you think of if it learns about you and becomes a better psychiatrist or something, then that's a switching cost."  Tactical:  Explore how AI learning can create network economies where one user's data improves the experience for all others.

View all skills from Hamilton Helmer →

Guillermo Rauch 1 quote

Listen to episode →

"When you're building AI products, it's a constant stream of user feedback. So for people that are thinking about not building AI products, it's going to be hard to compete with something that has such a tight feedback loop with users. The whole idea is to capture users' feedback so the next iteration of the model, the prompt, the fine-tuning, the examples, the rag is better."  Tactical:  Build infrastructure to capture user 'thumbs up/down' to inform the next iteration of fine-tuning.Treat user feedback as direct input for RAG (Retrieval-Augmented Generation) improvements.

View all skills from Guillermo Rauch →

Gustav Söderström 2 quotes

Listen to episode →

"The internet started with curation... then the world switched from curation to recommendation... And I think what we're entering now is we're going from your curation to recommendation to generation. And I suspect it will be as big of a shift that you will eventually have to rethink your products."  Tactical:  Identify 'zero intent' use cases where users don't know what they want and use generative AI to fill the gapDifferentiate between using AI for iterative improvements (safety, classification) versus core generative features    "The way to think about these diffusion models if and when they get good enough at generating music is probably the same like an instrument. It's just a much more powerful instrument and we'll probably see a new type of creator that wasn't proficient at any instrument."  Tactical:  Focus on how AI can help creators be 'truly unique' rather than just generating generic contentLook for new business models that allow rights-holders to benefit from generative technology

View all skills from Gustav Söderström →

Hilary Gridley 1 quote

Listen to episode →

"Designing reward loops... The reward loop needs to be powerful, it needs to be immediate, and it needs to be emotional, so that when this person does the thing that you want them to do, they feel like a million bucks. ... I like Custom GPTs as a tool for helping people learn to use LLMs... because they get the joy of like, 'Oh, this helps me. This was cool,' without any of the despair of, 'Oh, I'm not very good at prompting.'"  Tactical:  Start with fun, low-stakes AI use cases (e.g., vacation planning) to build the habit.Provide pre-built custom GPTs so users get immediate value without needing to master prompting first.Ensure the AI output provides a 'million bucks' feeling of accomplishment or time saved.

View all skills from Hilary Gridley →

Inbal S 5 quotes

Listen to episode →

"The user of the AI tools to develop software needs to form a different thinking. You need to start figuring out how are you using these AI tools to help you be successful. And it's no longer just the actual code writing, it's really evolving your thinking to the big picture, to the connected experience, to connected systems"  Tactical:  Focus on understanding the system and environment rather than just syntaxLeverage AI to handle simple code so junior developers can learn architecture earlier    "Generative AI will replace humans. I don't see that happening in the near future. The way I think about it, you always need that human in the loop because AI cannot replace innovation. That creative spark, that creative thinking that is the center of humanity, this will not be replaced by AI"  Tactical:  Keep a 'human in the loop' for all AI-generated outputsFocus human effort on innovation and creative problem solving rather than repetitive tasks    "What is that problem that we're trying to solve and how can we leverage AI better to help solve the problem versus what do we do with AI? So it's really working backwards from the customer problem from what we're trying to solve, and then realize what are the best tools that we have in order to do that work better"  Tactical:  Work backwards from the customer problem before selecting AI as the solutionIdentify manual or high-friction workflows as prime candidates for AI integration    "The design philosophy for Copilot is very much aligned with the working backwards concept... It's really putting yourself in the shoes of your customers and figuring out what is it that they need, how is that experience going to work for them? If it's an extra tool and if you need to ask for it and if you need to ask for it or if you need to wait for it, then developers will not adopt it."  Tactical:  Design AI features to be intuitive and frictionlessEnsure the AI assistant doesn't require the user to 'wait' or perform extra steps to get value    "There is no one metric to rule them all. It's a combination of the things that you're looking to measure out of adopting AI... productivity is not the right metrics against each one of these components. When we're implementing AI to GitHub Advanced Security, writing more secure code is the right element. It's like how many secrets were we able to prevent from leaking?"  Tactical:  Measure 'time to value' instead of just 'time saved'Use specific quality metrics like secrets prevented or bugs detected for security AI

View all skills from Inbal S →

Howie Liu 2 quotes

Listen to episode →

"How would you execute on that mission using a fully AI native approach? If you can't, then you should find a buyer and then if you really care about this mission, go and start the next carnation of it."  Tactical:  Ask: 'How would an AI-native company execute on our mission?'Use AI as a 'DSL' (Domain Specific Language) to manipulate existing product primitives rather than generating everything from scratchPrioritize 'vibe coding' and agentic app building over traditional GUI-only interfaces    "I think to really understand the solution space of what's possible, you have to be in the details. I mean, literally, you can't just look at screenshots or a pre-recorded video of a new product feature. AI is something you have to play with"  Tactical:  Play directly with underlying primitives via API or chat interfaces to understand model boundariesFocus on creating visual metaphors and affordances that help users understand underlying AI capabilities

View all skills from Howie Liu →

Ivan Zhao 2 quotes

Listen to episode →

"I always feels like AI language model feels like a new type of wood. It feels like aluminum. It's a new type of material... Mass air travel wasn't available until aluminum become cheap enough that people can make airplanes that support this at cost... AI is really good with bundled offerings. AI is really good with horizontal tools."  Tactical:  Leverage AI's ability to reason across disparate data sets to strengthen a horizontal product's value proposition.Build AI 'connectors' to pull external data into your core ecosystem to increase the AI's reasoning power.    "The first product was our AI writer product. Second product is AI Q&A or connectors. Please look at all the information in Notion and give your answer... the third one, which is even more fascinating... if we're just putting AI coding agent on top of it, you can create any kind of knowledge, customer software, customer agent for whatever your vertical use cases you need."  Tactical:  Sequence AI features from low-complexity (writing) to high-complexity (autonomous agents).Use AI to solve the 'blank slate' problem of modular tools by having it assemble components for the user.

View all skills from Ivan Zhao →

Jake Knapp + John Zeratsky 1 quote

Listen to episode →

"We found that it's especially valuable for AI startups. So it just turns out that a lot of the complex issues you have to figure out with turning something that may not initially be trustworthy may require a big behavior shift to customers who aren't used to working in this way and sometimes artificial intelligence can produce things that feel kind of alien to people. And so making this stuff actually useful, more than just a chatbot with little stars that's in the corner... but something that's really meaningful."  Tactical:  Focus on making AI features 'meaningful' rather than just adding generic chatbots.Address the 'trust hurdle' when introducing AI into traditional workflows.

View all skills from Jake Knapp + John Zeratsky →

Jason Droege 2 quotes

Listen to episode →

"The general trend right now is going from models knowing things to models doing things. The next question becomes, what can it do for me? How does the agent make decisions for you?"  Tactical:  Focus product development on agentic workflows where models navigate software environmentsDesign systems that allow agents to pop up to humans for feedback when accuracy is low    "These things take 6 to 12 months to get them truly robust enough where an important process can be automated. Like with any of these major tech revolutions, headlines tell one story and then on the ground, laying broadband means you need to dig up every single road in America to lay it."  Tactical:  Plan for long implementation cycles beyond the initial proof-of-concept (POC)Focus on reliability and 'five nines' accuracy for mission-critical processes

View all skills from Jason Droege →

Jonathan Becker 1 quote

Listen to episode →

"The effect ultimately that we've seen from a human capital point of view is displacement. We have more people now than we've ever had, but the nature of the work that they do is more strategic. It's more about modeling, validation, asking the right questions, being focused around creative levers. And less so the like trench work of implementation and bid modifiers at the keyword level on Google search, and some of the really hardcore manual analysis we had to do."  Tactical:  Focus human capital on strategic modeling and validationAutomate manual tasks like bid modifiers and keyword-level analysis

View all skills from Jonathan Becker →

Karina Nguyen 4 quotes

Listen to episode →

"Creative thinking and you kind of want to generate a bunch of ideas and filter through them and not just build the best product experience. I think it's actually really, really hard to teach the model how to be aesthetic or really good visual design or how to be extremely creative in the way they write."  Tactical:  Focus on developing 'aesthetic' and 'creative' judgment that models currently lack.    "Because file uploads... It's like form follows function. It's like the form factor, the file uploads can enable people to just literally upload anything, the books, any reports, financial and ask any task to the model."  Tactical:  Design form factors that align with familiar user tasks (e.g., uploading a document) to unlock model utility.    "You want to build for the future. So it's like it doesn't necessarily matter whether the model is good or not, good right now, but you can build product ideas such that by the time the models will be really good, it'll work really well."  Tactical:  Prototype product ideas that might fail today but will succeed as reasoning costs drop and intelligence increases.    "I think what models are really good at is connecting the dots, I think. It's like if you have user feedback from this source, but you also have an internal dashboard with metrics and then you have other feedback or input and then it can create a plan for you, recommendations even."  Tactical:  Use LLMs to aggregate and summarize user feedback and internal metrics to identify the most painful user flows.

View all skills from Karina Nguyen →

Keith Coleman & Jay Baxter 1 quote      "take existing notes as input... have an LLM generate a ton of different variants, and then basically make the simulated jury to basically get a representative group of contributors for community notes who would be rating the note and try to predict based on their past ratings how they would rate these LLM generated notes."  Tactical:  Use LLMs to generate multiple variants of a piece of content based on existing user inputsSimulate user rating processes using historical data to predict which AI-generated content will be most helpful

View all skills from Keith Coleman & Jay Baxter →

Kevin Weil 4 quotes

Listen to episode →

"Everywhere I've ever worked before this, you kind of know what technology you're building on... but that's not true at all with AI. Every two months, computers can do something they've never been able to do before and you need to completely think differently about what you're doing."  Tactical:  Expect the technology to change every two monthsRe-evaluate product direction based on new model capabilities frequently    "Our general mindset is in two months, there's going to be a better model and it's going to blow away whatever the current set of limitations are... If you're building and the product that you're building is kind of right on the edge of the capabilities of the models, keep going because you're doing something right."  Tactical:  Don't over-engineer scaffolding for current model limitationsBuild products that push the current edge of model capabilities    "I think the future is really going to be incredibly smart, broad-based models that are fine-tuned and tailored with company-specific or use case-specific data so that they perform really well on company-specific, or use case-specific things."  Tactical:  Identify non-public data that can be used for fine-tuningDevelop custom benchmarks to measure performance on specific use cases    "We use ensembles of models much more internally than people might think... If we have 10 different problems, we might solve them using 20 different model calls, some of which are using specialized fine-tuned models... You want to break the problem down into more specific tasks versus some broader set of high level tasks."  Tactical:  Break down broad problems into specific sub-tasksUse different model sizes (e.g., 4o vs 4o mini) based on latency and cost needs for each sub-task

View all skills from Kevin Weil →

Luc Levesque 1 quote

Listen to episode →

"What we're about to see is basically Google... showed a big box on top of the search results that answers the query directly... how do you optimize in a world where it's not so much about optimizing for the platform, but teaching the AI what you do and why you're the best in the world at it."  Tactical:  Identify 'informational' keywords at risk of being cannibalized by AI search summariesShift focus toward 'transactional' intent where users still need to click through to complete an action

View all skills from Luc Levesque →

Madhavan Ramanujam 2 quotes

Listen to episode →

"AI pricing is very different from the previous vintage of companies... we have moved from software being a pay for access to now you're paying for work delivered. So the monetization model's become key."  Tactical:  Focus on 'pay for work delivered' rather than 'pay for access'Solve the 'attribution problem' by showing exactly how the AI impacts customer KPIs    "What that would mean is, how do I build functionality in the products to actually show attribution, how do I build more agentic workforces to take the human out of the loop and be more autonomous, and being thoughtful about your vision and strategy so that you will orient yourself towards more outcome-based pricing models."  Tactical:  Build dashboards that showcase value attribution to customer KPIsDevelop agentic capabilities to move from 'copilot' to 'autonomous' mode

View all skills from Madhavan Ramanujam →

Logan Kilpatrick 4 quotes

Listen to episode →

"I'm really, really excited to see more people. I think 2024 is the year of multimodal AI, but it's also the year that people really push the boundaries of some of these new UX paradigms around AI."  Tactical:  Explore interfaces like 'infinite canvases' where AI can populate details, files, and videos in a non-linear format.Look beyond the predominant chat interface to find more human-centric ways of interacting with data.    "I think GPTs is our first step towards the agent future. Again, today when you use A GPT, it's really you send a message, you get an answer back almost right away... I think as GPTs continue to get more robust, you'll actually be able to say, 'Hey, go and do this thing and just let me know when you're done.'"  Tactical:  Design products that allow users to delegate tasks to the AI and receive notification upon completion rather than requiring active waiting.Build for a future where AI spends more 'thought time' on meaningful requests.    "I heard from a friend that there's kind of this tip that when you're building products today, you should build towards a GPT-5 future, not based on limitations of GPT-4 today."  Tactical:  Assume future models will be faster, smarter, and solve higher echelons of problems.Plan for a world where AI tools become 'normal' and integrated very quickly rather than assuming they will remain a novelty.    "I think products that move beyond this chat interface really are going to have such an advantage. And also, thinking about how to take your use case to the next level... What I really want is just ask my question... Get an answer to that question in a very data grounded way."  Tactical:  Identify areas where users currently navigate complex UI filters and replace them with a single natural language query.Focus on providing a summary of 'what is happening' in the data rather than just showing raw examples.

View all skills from Logan Kilpatrick →

Marc Benioff 2 quotes

Listen to episode →

"AI is the defining technology of our lifetime and probably any lifetime."  Tactical:  Treat AI as the primary lens for all future product development    "Step one was we had to automate all these customer touch points... step three is the agentic platform on top of that. Then, the fourth layer that will come will be the robotic drone layer where those robots and drones will then feed off of the platform and all of these capabilities."  Tactical:  Automate customer touchpoints first to create a baseline of interactionAggregate all interaction data into a unified 'Data Cloud'Build an 'agentic' layer on top of the data to handle autonomous tasks

View all skills from Marc Benioff →

Marily Nika 3 quotes

Listen to episode →

"I believe that ballpark managers will be AI product managers in the future. And this is because we see all products needing to have a personalized experience, a recommender system that is actually good."  Tactical:  Anticipate that every product will eventually require a personalized experience or recommender system.Prepare for a future where 'AI PM' and 'Generalist PM' roles merge.    "Don't do it for your MVP. It makes zero sense. Do not waste time of data scientists that can train models with using powerful machines that are going take weeks to train. This is because if you have an MVP and you just want to get buy-in for an idea or feature that may use AI in the future, take it, create a little figma prototype and just show it some users, just fake what the AI is going to be doing."  Tactical:  Use Figma prototypes to simulate AI features for initial user testing.Only invest in training models once you have validated the problem and have sufficient data.    "AI product development is different. As I mentioned before, sometimes you're actually managing the problem and not the product and you're trying to secure out if there is a problem that makes sense to be answered by a smart solution."  Tactical:  Clarify with leadership that progress in AI/Research may not always result in a launch.Be prepared to pivot or shut down projects if the model results don't meet the hypothesis.

View all skills from Marily Nika →

Marty Cagan 1 quote

Listen to episode →

"I've been on so many of these calls where we've been talking about the implications of probabilistic software versus deterministic software and what is okay? The lawyers are weighing in already with the legal perspective, but also ethical perspective and just if this is mission critical, is this something that we could be okay with having a probabilistic answer?"  Tactical:  Evaluate the risks of using probabilistic AI answers in mission-critical features.Involve legal and ethical perspectives early when defining AI product strategy.

View all skills from Marty Cagan →

Matt MacInnis 1 quote

Listen to episode →

"Point solutions don't have enough data in the age of AI to be useful. You got to be able to provide the AI with a lot of context about a lot of data so it can do things. It can do joins. It can do correlations."  Tactical:  Focus on building a 'common business data graph' to give AI the context it needs to be useful.Avoid building AI point solutions that rely on 'drinking data through a straw' via limited integrations.

View all skills from Matt MacInnis →

Matt Mullenweg 2 quotes

Listen to episode →

"Llama, you can obviously download and run locally and all these sorts of things, right? You don't have to use their SaaS service. However, there's a clause in it that says if you're above a certain threshold of monthly active users... You need a license from them. And so that does not give you the freedom to use the software for any purpose."  Tactical:  Audit AI model licenses for 'user threshold' clauses that might restrict future growthDistinguish between 'open weights' and true 'open source' when selecting foundational models    "But I can't wait for more automated scanning there, and I think that could vastly upgrade the security of open source. The other thing that's really exciting is right now you see people building apps and stuff and it's just sort of custom generated code, but I think the next generation of these models... is when the open source models you say like, 'Hey, build me a website.' It actually installs WordPress, and then builds on top of that."  Tactical:  Use AI to automate security scanning of third-party plugins and extensionsDirect AI agents to build on top of audited open-source platforms to ensure long-term maintainability

View all skills from Matt Mullenweg →

Mayur Kamat 1 quote

Listen to episode →

"At a company level, there is an incredible set of advancements across these three areas: developer productivity, customer support, and fraud."  Tactical:  Deploy AI co-pilots to achieve a 20-25% boost in developer productivity.Use LLMs to automate the 'bottom 70%' of customer support queries.Apply AI to detect language and transaction patterns in fraudsters.

View all skills from Mayur Kamat →

Melanie Perkins 1 quote

Listen to episode →

"I think being able to integrate it into the product where it actually helps people to get their work done where it genuinely helps them to achieve their goals... AI is just kind of naturally a very critical part of that equation for us."  Tactical:  Embed AI tools directly into the core editor or 'elements' tabs where users already workPrioritize AI features that solve specific user requests (e.g., safety controls for teachers)

View all skills from Melanie Perkins →

Michael Truell 2 quotes

Listen to episode →

"At this point, every magic moment in Cursor involves a custom model in some way... picking your spots carefully, not trying to reinvent the wheel, not trying to focus on places, and maybe where the best foundation models are excellent, but instead kind of focusing on their weaknesses, and how you can complement them."  Tactical:  Use custom models for tasks requiring high speed (e.g., Focus custom model development on the weaknesses of foundation models rather than trying to replicate their general intelligence.    "We take the sketches of the changes that these models are suggesting, you make with that code base. And then we have models that then fill in the details of, the high level thinking is done by the smartest models, they spend a few tokens on doing that, and then these smaller specialty incredibly fast models, coupled with some inference tricks, then take those high level changes and turn them actually into full code diffs."  Tactical:  Use high-reasoning models (like Sonnet or GPT-4) for high-level 'sketches' of work.Use smaller, faster models to fill in the technical details and generate final outputs.

View all skills from Michael Truell →

Mihika Kapoor 1 quote

Listen to episode →

"I think that the key to being successful at zero-to-one is to honestly have optimism that borders on delusion. You need to be insane, almost like reality distortion field where you don't hear the word no, or at the very least, you translate it into a not yet."  Tactical:  Focus on 'black-boxification'—making AI outputs interactive and manipulatable rather than staticLook for distribution or platform advantages when deciding whether to build inside an existing companyUse hackathons to rapidly prototype and secure initial buy-in for ambitious new product directions

View all skills from Mihika Kapoor →

Mike Krieger 3 quotes

Listen to episode →

"The functional unit of work at Anthropic is no longer take the model and then go work with design and product to go ship a product. It's more like we are in the post-training conversations around how these things should work and then we are in the building process and we're feeding those things back and looping them back."  Tactical:  Embed product managers directly with researchers during the fine-tuning and post-training phases.Focus on the intersection of model capabilities and product experience rather than just prompting off-the-shelf models.    "I think there's still a lot of value in two things. One is making this all comprehensible... Two is... strategy, how we win, where we'll play... And then the third one is opening people's eyes to what's possible, which is a continuation of making it understandable."  Tactical:  Focus on reducing the 'overhang'—the gap between what models can do and how users actually use them.Prioritize empathy and human psychology to make AI capabilities understandable for non-technical users.    "I think things that are going to, I can't promise this as a five to 10 year thing, but at least one to three years, things that feel defensible or durable. One is understanding of a particular market... Two was paired with that is differentiated go to market... Then the last one is... a completely different take on what the form factor is by which we interface with AI."  Tactical:  Build products for specific industries (e.g., legal, biotech) with complex compliance or workflow needs.Experiment with 'weird' or power-user form factors that incumbents are too slow to adopt.

View all skills from Mike Krieger →

Naomi Ionita 1 quote

Listen to episode →

"I think what I described around marketing and sales, just because they really touch the dollars. It can be this ROI story around saving time, but also driving revenue. There'll be plenty of really effective examples within things like customer support. I mean the cost savings potential. There's going to be massive."  Tactical:  Focus AI implementation on revenue-generating or high-cost-saving functions like SDR outbounding or customer support

View all skills from Naomi Ionita →

Nick Turley 5 quotes

Listen to episode →

"I've never ever worked on a product that is so empirical in its nature where, if you don't stop, and watch, and listen to what people are doing, you're going to miss so much, both on the utility and on the risks, actually. Because normally, by the time you ship a product, you know what it's going to do... And with AI, because I think so much of it is emergent, you actually really need to stop and listen after you launch something."  Tactical:  Observe user behavior post-launch to identify emergent utility and risksIterate on the model based on real-world use cases rather than a priori reasoning    "One thing we've learned with ChatGPT is that there really is no distinction between the model and the product. The model is the product and therefore you need to iterate on it like a product."  Tactical:  Systematically improve the model for specific high-value use cases like coding or writingTreat 'vibes' and personality as product features to be tuned    "I think that in the original release, making it free was a big deal... making it free and putting a nice UI on it, very consequential in the way that you take for granted now. And this is why I think that A, distribution and the interface are continuously important even in 2025."  Tactical:  Prioritize removing friction (like login requirements) to drive growthUse a free tier to gather the massive data needed for model iteration    "If we're shipping a feature and it doesn't get 2X better as the model gets 2X smarter, it's probably not a feature we should be shipping."  Tactical:  Evaluate features based on their ability to benefit from future model intelligence gainsFocus on 'interdisciplinary' development where research and product goals align    "I started writing evals before I knew what an eval was because I was just outlining very clearly specified ideal behavior for various use cases... it might be the lingua franca of how to communicate what the product should be doing to people who do AI research."  Tactical:  Articulate success by outlining ideal model behaviors for specific use casesUse evals as a bridge between product requirements and technical research

View all skills from Nick Turley →

Nicole Forsgren 2 quotes

Listen to episode →

"People really fundamentally shift the way they work when they work with an AI-enabled tool... you spend more time reviewing code than writing code... we've changed what your mental model is. So we've changed the friction model that you expect. We've changed the cognitive load of what you expect."  Tactical:  Evaluate AI tools based on how they free up cognitive space for harder tasks rather than just time saved on simple tasks.Consider new dimensions of productivity like 'trust' and 'reliability' when integrating AI into the workflow.    "I think there are a lot of ways that we can pull in AI tools to help us refine our strategy, refine our message, think about the experimentation methods or targets of experimentation... because now, the engineering can go, or at least the prototyping especially, much, much faster. We can throw out prototypes. We can run any tests and experiments that are customer facing"  Tactical:  Use AI to rapidly generate and test multiple strategic alternatives or prototypes.Shorten the feedback loop from idea to production experiment to under a week using AI acceleration.

View all skills from Nicole Forsgren →

Noah Weiss 2 quotes

Listen to episode →

"One of the big ones, was that the promise of the UI has to match the quality of the underlying data, which is to say... I think this is actually one of the failings of the various LMs right now is they all appear supremely confident even when they're completely hallucinating. I think that's going to be something that people are going to have to work on a lot, which is to figure out how to be not so faultless, to acknowledge when you're not sure."  Tactical:  Acknowledge uncertainty in AI responses rather than appearing 'supremely confident' when hallucinating.Provide transparency about where data comes from to build credibility.    "What we want to do is actually spin up a couple different teams that are focused on prototyping, using that common infrastructure but in specific directions that are all a little bit different. We've got a common ML, let's say in search team and now we have a bunch of teams that are working in parallel and different customer problems that we're trying to solve using that shared infrastructure."  Tactical:  Use a hybrid model: central ML infrastructure + decentralized prototyping teams.Give AI prototyping teams a 'get out of jail free card' from normal quarterly planning to increase learning velocity.

View all skills from Noah Weiss →

Noam Lovinsky 1 quote

Listen to episode →

"Grammarly is one of the few products where you just install it and it makes you better. You don't have to configure it, you don't have to manipulate it, you don't have to change anything about what you're doing. ... essentially it's like a huge AI achievement masquerading as a little UX innovation."  Tactical:  Design AI features that integrate into existing workflows rather than requiring new onesFocus on 'invisible' AI that provides value without complex prompting or setup

View all skills from Noam Lovinsky →

Paul Adams 3 quotes

Listen to episode →

"I'd start with the thing your product does. "What's the core premise behind it? Why do people use it? What problem does it solve for them?" That kind of thing. So, go back to basics. And then ask, "Can AI do that?" And for a lot, the answer is going to be, "Yes, it can.""  Tactical:  Identify the core problem your product solves.Determine if AI can replace the current solution or merely augment it.    "You're going to need to map what your product does against what AI can do... for some of it'll be replacement. AI would replace, it'll just do it. And, in other places, it'll be augmentation. It'll augment. It'll help people."  Tactical:  Map product features against AI's ability to write, summarize, reason, and take actions.    "Don't bolt it on. I think some people are still in that camp... Don't be like, "Oh, we'll have a bunch of AI people..." And we do have some specialists. But generally speaking, we're trying to have everyone learn about it."  Tactical:  Encourage generalist PMs and engineers to learn AI interfaces and frameworks.Avoid creating a 'side team' that only adds AI features to existing products.

View all skills from Paul Adams →

Ramesh Johari 2 quotes

Listen to episode →

"Predicting is about picking up patterns, but making decisions, it's about thinking about these differences... the first and most important thing that I feel very strongly about in what would I get a data scientist to do is... get them to be thinking in the back of their mind always that their goal is to help the business make decisions. And that the distinction between causation and correlation matters a lot."  Tactical:  Shift the data team's focus from building predictive models to identifying the causal impact of specific product changes.    "What AI has done for us is it's massively expanded the frontier of things we could think about our problem, hypotheses we could have, maybe things we could test... I really think actually what that does is puts more pressure on the human, not less. I think it becomes more important for humans to be in the loop in interacting with these tools to drive the funneling down process of identifying what matters."  Tactical:  Use AI to generate a vast array of testable hypotheses or creatives, but maintain human oversight to select which ones align with strategic goals.

View all skills from Ramesh Johari →

Ravi Mehta 1 quote

Listen to episode →

"I think one of the most interesting things about it is not AI as a replacement for people, but AI as a way to amplify people and make them more effective. And I think we'll see a lot of that in terms of both image generation and text generation where it's less about AI doing all the work and more about AI providing a really good starting point."  Tactical:  Use AI to generate initial drafts or suggestions (e.g., coaching feedback) that experts then tailor.Experiment with different prompting styles (e.g., action-oriented vs. sympathetic) to simulate different personas or leadership styles.

View all skills from Ravi Mehta →

Rahul Vohra 1 quote

Listen to episode →

"I think for me the biggest surprise has been how unpredictable the user love has been in terms of what they love and what they don't love... everything I thought would work out well, people use it less than they thought they did. And everything where I was like, 'I don't know, but let's build the thing,' people love that."  Tactical:  Experiment with 'commodity' AI features like writing assistance, as they often have the highest utility.Be prepared to pivot the AI roadmap based on actual usage data rather than founder intuition.

View all skills from Rahul Vohra →

Roger Martin 1 quote

Listen to episode →

"It is super hard when the guts of how you make money is under threat, and you just don't want that thing to go away... But my general advice is always the same, which is, it can take a while, but in the end the customers will triumph."  Tactical:  Identify where the 'customer tide' is moving, even if it threatens your current business model.Avoid trying to 'hold back the tide' of new technology; instead, scramble to find how to serve customers in the new reality.

View all skills from Roger Martin →

Robby Stein 2 quotes

Listen to episode →

"AI is expansionary. There's actually just more and more questions being asked and curiosity that can be fulfilled now with AI."  Tactical:  Identify use cases where users are currently 'hacking' your product (e.g., adding 'AI' to search queries) to find where AI can add value.Focus AI features on expansionary moments rather than just replacing core foundational needs.    "We wanted to be the best at informational needs, that's what's Google's all about, and so how does it find information? How does it know if information is right? How does it check its work? These are all things that we built into the model."  Tactical:  Build 'check your work' mechanisms into models to ensure accuracy for informational tasks.Use query fan-out to allow models to use search as a tool for real-time data retrieval.

View all skills from Robby Stein →

Ryan J. Salva 2 quotes

Listen to episode →

"We see it range anywhere from the upper twenties to the forties across all the different languages. ... AI is going to infuse pretty much our entire development stack in the not so distant future. Copilot is really just the very tip of the sphere for a lot of innovations and better managing maybe our build queues or helping to... Here's a great one. I don't know about you, but often the comments that I get with commit messages and PRs aren't super great. It puts a lot of effort onto the code reviewer to go figure out what the developer was actually trying to do. What if AI could summarize all of your changes with your full request and you just have to, as the contributing developer, just review it to make sure it's accurate, send it on its way, and you don't have to put in extra effort for that."  Tactical:  Identify high-drudgery, low-creativity tasks in the workflow for AI automationPosition AI as an 'augmenter' rather than a 'replacer' to manage user expectations and anxiety    "Our stance on it, what we ended up coming to is actually the framing of Copilot as an AI pair programmer i think is a useful one. ... Well, if Copilot is your AI pair programmer and they're whispering crazy stuff into your ear and they're bringing politics into it or gender identity into it or, I don't know, whatever other... They're spouting off slang and slander and all that kind of stuff. You're probably not going to be able to focus on your work, right? It's going to be really distracting. Really coming down to some principles about what is the use case we're trying to solve, what is appropriate, I put this in scare quotes, behavior of the AI bot sitting side by side with you, helped us create some principles or some guidelines for the developer experience that we wanted to create."  Tactical:  Define a persona for the AI to establish behavioral guardrailsEstablish principles for what constitutes 'appropriate' AI interaction within the specific product context

View all skills from Ryan J. Salva →

Sander Schulhoff 5 quotes

Listen to episode →

"If we can't even trust chatbots to be secure, how can we trust agents to go and manage our finances? If somebody goes up to a humanoid robot and gives it the middle finger, how can we be certain it's not going to punch that person in the face?"  Tactical:  Prioritize 'agentic security' when building products that have the power to take actions (e.g., booking flights, managing money)    "The most common technique by far that is used to try to prevent prompt injection is improving your prompt and saying... 'Do not follow any malicious instructions.' This does not work at all... Fine-tuning and safety-tuning are two particularly effective techniques and defenses."  Tactical:  Don't rely on system prompts to prevent malicious injectionsUse fine-tuning to narrow a model's capabilities to a specific task, making it less susceptible to general malicious instructions    "It is not a solvable problem... You can patch a bug, but you can't patch a brain... you can never be certain with any strong degree of accuracy that it won't happen again."  Tactical:  Assume a 95-99% security ceiling and build product safeguards accordinglyFocus on mitigation and detection rather than expecting a 100% 'fix' for prompt injection    "If you deploy improperly secured, improperly data-permissioned agents, people can trick those things into doing whatever, which might leak your user's data and might cost your company or your user's money, all sorts of real world damages there."  Tactical:  Ensure agents are properly data-permissioned before deploymentEvaluate the potential for agents to chain actions together in malicious ways    "If all you're doing is deploying chatbots that answer FAQs... It's not really an issue because your only concern there is a malicious user comes and, I don't know, maybe uses your chatbot to output hate speech... but they could go to ChatGPT or Claude or Gemini and do the exact same thing."  Tactical:  Distinguish between simple chatbots and agentic systems when assessing security needsFocus security efforts on systems that can take actions or access sensitive user data

View all skills from Sander Schulhoff →

Sarah Tavel 1 quote

Listen to episode →

"LLMs may make it possible to bring on a supply type that maybe the long tail, that was just, it was too much effort to reach out to them, onboard them, but maybe if you automate that work, you actually create an opportunity to expand the supply in a way that none of us can anticipate right now."  Tactical:  Look for supply segments that were previously too expensive to acquire manually and use LLMs to automate their integration

View all skills from Sarah Tavel →

Shaun Clowes 2 quotes

Listen to episode →

"LLMs can only be as good as the data they are given and how recent that data is. They're ultimately like information shredders. They are limitless information eaters. You can never have enough information to give to an LLM to truly gain its value."  Tactical:  Prioritize building data pipelines that feed high-quality, real-time context to LLMs over simply choosing the 'best' model.    "It's a data management problem. It's getting access to good data, getting access to high quality data, getting access to timely data and getting it to the LLM to get the LLM to make a smart decision. That's where 90% of the calories go."  Tactical:  Invest 90% of effort into data quality and accessibility for the AI rather than just UI or prompt engineering.

View all skills from Shaun Clowes →

Shweta Shriva 1 quote

Listen to episode →

"We're using a lot of human driving data to train our deep models. So it's important to make sure that the behavior of the car doesn't seem robotic... we have deep learned models that can understand what the other road users' intent is. So, stuff like which way the pedestrian is looking or what is their body orientation because that could tell you which way they're headed."  Tactical:  Use human behavior data to train models to avoid unnatural or 'robotic' product interactions.Incorporate intent recognition (e.g., body orientation, gaze) into AI models to handle complex human environments.

View all skills from Shweta Shriva →

Tomer Cohen 4 quotes

Listen to episode →

"What is the objective of the algorithm? I would challenge you to ask folks... what is the objective of the algorithm and can you write it down for me on a board? They should be able to do so, ultimately it's a mathematical formula and then it's like what features have you added to the algorithm? ...what investment do you have in data collections and fine-tuning?"  Tactical:  Define the mathematical objective of the algorithm as a core product requirement.Invest in infrastructure and data collection as primary product levers rather than just UI features.Shift from controlling the exact user experience to controlling the 'ingredients' (data and guidelines) that the AI uses.    "AI is the ultimate matchmaker. It's underutilized, it's misunderstood... in a marketplace it's all about value exchange. And if I'm able to do value exchange really well, then people will come back and they do and they engage."  Tactical:  Focus AI objectives on downstream value (e.g., meaningful conversations) rather than just top-level clicks.    "We call it the full stack builder model. The goal itself is to empower great builders to take their idea and to take it to market, regardless of their role and the stack and which team they're on. It's really fluid interaction between human and machine."  Tactical:  Empower builders to work across traditional functional boundariesFocus human effort on vision, empathy, communication, creativity, and judgmentAutomate repetitive process steps to increase iteration speed    "The platform for us as an example is rearchitecting all of our core platforms so AI can reason over it. So we're building kind of this composable UI components with server side that we actually build. We're basically building for AI to be ready to bring it in."  Tactical:  Rearchitect core platforms for AI readabilityBuild composable UI components that AI can assembleCustomize third-party AI tools to work with internal proprietary stacks

View all skills from Tomer Cohen →

Varun Mohan 3 quotes

Listen to episode →

"We should be cannibalizing the existing state of our product every six to 12 months. Every six to 12 months, it should make our existing product look silly. It should almost make the form factor of existing product look dumb."  Tactical:  Plan for major product paradigm shifts every 6-12 monthsInvest in long-term R&D that might render current features obsolete    "Where is the layer that you can actually differentiate on? And we believe the application layer is a very, very deep layer to go out and differentiate on. What are the number of ways we can build better user experiences and better workflows for developers? We think there's effectively no ceiling on that."  Tactical:  Focus on vertical integration and custom UI/UX rather than just being a model wrapperIdentify specific user workflows that can be fundamentally reimagined with AI    "If AI is writing over 90% of the code... the ROI of building technology has actually gone up. This actually means you hire more. The best thing to do is just get your hands dirty with all of these products. You could be a force multiplier to your organization in ways in which they never even anticipated."  Tactical:  Use AI to increase the volume and complexity of technology the organization can produceEncourage non-technical roles to use AI tools to build custom internal solutions

View all skills from Varun Mohan →

Brendan Foody 2 quotes

Listen to episode →

"If the model is the product, then the eval is the product requirement document. And the way that researchers' day-to-day looks is that they'll run dozens of experiments where they'll make small improvements on an eval set."  Tactical:  Treat evals as the PRD for AI productsRun iterative experiments to make small, measurable improvements against an eval set    "I think that for enterprises especially, the core way to think about it is how can they build a test or systematic way to measure how well AI automates their core value chain?"  Tactical:  Identify the core value chain of the businessBuild a systematic test to measure AI's performance in automating that specific chain

View all skills from Brendan Foody →

Andrew Wilkinson 1 quote

Listen to episode →

"I think the fundamental question is, do all jobs just become a single prompt? For example, does a CEO just grow the business while making the customers happy and turning a profit... and it is able to actually be an omniscient presence that can run a whole company."  Tactical:  Prepare for a future where AI models may be 'smarter than all PhDs' by 2027.Focus on building wealth and diversifying into compute and energy as AI drives down the cost of labor.Identify 'human-only' value adds like humor, status, and physical connection in a world of AI abundance.

View all skills from Andrew Wilkinson →

Garrett Lord 2 quotes

Listen to episode →

"The models have gotten so good that the generalists are no longer needed. What they really need is experts, experts across every area that the models are focused on."  Tactical:  Focus on advanced STEM domains and derivative professional functions like law and medicine for model improvementTarget experts (PhDs, Masters) who can identify where models break in reasoning or ground truth    "We like to say the only moat in human data is access to an audience. Basically, there are many, many small players in this space... they're basically running TikTok ads... The huge advantage that we've had... is we built a decade of trust with 18 million people."  Tactical:  Leverage existing brand affinity to lower customer acquisition costs for data contributorsUse historical data on user performance to target the right experts for specific labeling tasks

View all skills from Garrett Lord →

Paige Costello 1 quote

Listen to episode →

"When it came to the massive leap forward in LLMs recently, we staffed a team to really prototype quickly, and discover what was possible, and just apply hypotheses outside of the typical norms of how we work. So they went straight to prototyping instead of going through that Double Diamond I was explaining earlier."  Tactical:  Staff a dedicated team to prototype AI hypotheses outside of normal product cycles.Skip formal discovery phases in favor of immediate prototyping when dealing with high-uncertainty technology.

View all skills from Paige Costello →

Peter Deng 3 quotes

Listen to episode →

"A lot of the value is still going to require a bunch of hustle from a lot of builders to really turn that new source of energy and channel it into something that we humans want to use that solves some of our problems."  Tactical:  Focus on the 'elbow grease' required to turn raw AI intelligence into a useful productIdentify specific human problems that AI can solve more ergonomically than existing tools    "The data flywheel thing is really interesting because the models will get really good at whatever data you show it... being very mindful of the data that you have access to to start your flywheel going and what you can do to keep on going with that flywheel is going to be a critical thing."  Tactical:  Identify proprietary data sources to start the initial model training flywheelBuild workflows that naturally generate more high-quality data through user interaction    "I think that close, tight-knit relationship at any of these large model companies between post training and product is going to produce some really incredible stuff."  Tactical:  Embed PMs within research teams to influence model 'vibe' and capabilitiesFocus on fine-tuning and post-training rather than just the UI layer

View all skills from Peter Deng →

Scott Belsky 1 quote

Listen to episode →

"I think that the greatest performers I've ever worked with... preserve the time to explore lots of possibilities... generative AI and AI for all, when it talks to me about just product leaders exploring possibilities, this should expand the surface area."  Tactical:  Use AI to generate multiple 'what if' scenarios to expand your thinking beyond your initial solutionTreat AI as an 'intern' to create initial drafts or thumbnails that you then refinePlay with emerging AI tools regularly to understand how they can augment your specific creative process

View all skills from Scott Belsky →

Scott Wu 2 quotes

Listen to episode →

"I think the big shift that we really felt we would see is moving from kind of this text to text model to an actual autonomous system that can make decisions, that can interact with the real world, that can take in feedback, that can iterate and take multiple steps to solve problems. And now we call that agents, but that was what we were really excited about at the time."  Tactical:  Focus on building autonomous systems rather than just text-to-text completion toolsDesign for systems that can take in feedback and iterate on their own work    "I think the product experience itself is going to change every single time. And then obviously there, there's all of the practicality of just getting it out there in the world. And so folks obviously need to learn how to use the new technology. There's a lot to do to deploy into all of the messiness of real world software."  Tactical:  Anticipate that the product interface will need to change with every new generation of model capabilitiesPrioritize handling real-world complexity and 'messiness' over theoretical performance

View all skills from Scott Wu →

Timothy Davis 1 quote

Listen to episode →

"You guys have been using AI for years now. Smart Bidding is AI. All of the recommendations within Google Ads is AI. Ad copy recommendations is AI, and that's always been in the platform."  Tactical:  Leverage platform-native AI for bidding and ad copy iterations rather than seeking external tools for basic tasks

View all skills from Timothy Davis →

Tamar Yehoshua 2 quotes

Listen to episode →

"In five to 10 years, I think the lines between product managers and engineers and designers are going to blur because AI will enable product managers to build prototypes, to build designs... I'm of the believer that we're just going to have a lot more software."   "The industry is transforming so rapidly that you need to make sure that your product gets better as the LLMs get better. And that too many people are building things to make up and compensate for the LLMs that all that work is going to go away. So it's okay to do it to understand that it's going to go away, but that can't be your differentiator."  Tactical:  Ensure your product's unique value lies in something outside the base capabilities of the LLM (e.g., proprietary data access or specific workflows).

View all skills from Tamar Yehoshua →

Casey Winters 1 quote

Listen to episode →

"If you thought the PM job was just filling in frameworks, you're going to get replaced by AI."  Tactical:  Build subject matter expertiseUse AI for tedious work

View all skills from Casey Winters →

David Singleton 1 quote

Listen to episode →

"We can have GPT-4 read all our docs and answer questions for developers."  Tactical:  Use embeddings for docsTranslate natural language to technical queries

View all skills from David Singleton →

Jag Duggal 1 quote

Listen to episode →

"Companies need to figure out what AI native means, not how to append AI at the corners."  Tactical:  Ask what you'd design if AI existed from the startBuild AI at the heart

View all skills from Jag Duggal →

Krithika Shankarraman 1 quote

Listen to episode →

"Taste is going to become a distinguishing factor in the age of AI."  Tactical:  Invest in building tasteUse AI to augment not replace judgment

View all skills from Krithika Shankarraman →

Sam Schillace 1 quote

Listen to episode →

"AI isn't a feature of your product. Your product is a feature of AI."  Tactical:  Build products that require AIThink of AI as enabling new category

View all skills from Sam Schillace →

Install This Skill

Add this skill to Claude Code, Cursor, or any AI coding assistant that supports Agent Skills.

1  Download the skill

Download SKILL.md

2  Add to your project

Create a folder in your project root and add the skill file:

.claude/skills/ai-product-strategy/SKILL.md    3  Start using it

Claude will automatically detect and use the skill when relevant. You can also invoke it directly:

Help me with ai product strategy              Related Skills Other AI & Technology skills you might find useful.    60 guests    Building with LLMs Using LLMs for text-to-SQL can democratize data access and reduce the burden on data analysts for ad...  View Skill → →      24 guests    Platform Strategy Platform and ecosystem success comes from identifying 'gardening' opportunities—projects with inhere...  View Skill → →      22 guests    Evaluating New Technology Be skeptical of 'out-of-the-box' AI solutions for enterprises; real ROI requires a pipeline that acc...  View Skill → →      3 guests    Vibe Coding The guest repeatedly uses this term to describe a new mode of development where non-engineers (desig...  View Skill → →

AI Transformation Partner

Start Your Journey

SERVICES  AI Audit AI Automation AI Training    COMPANY  About Case Studies Book a Call

© 2026 Refound. All rights reserved.