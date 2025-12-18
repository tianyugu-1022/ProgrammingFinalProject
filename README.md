# Associative Memory Experiment
Associative memory refers to the ability to form and later retrieve links between separate pieces of information. Instead of remembering items in isolation, people often remember relationships, such as which word appeared with which other word, or which cue predicts a target. This kind of memory is central to everyday functioning (e.g., remembering a person’s name when you see their face) and is commonly studied using paired-associate or cued-recall tasks, where part of a learned episode is presented as a cue to trigger retrieval of the missing information.

---
## Aim of the Experiment
This word memory experiment is designed to examine associative memory. During an encoding phase, participants study words presented in grouped triplets. Memory is later assessed using a cued-recall task, in which the first two words from each triplet serve as retrieval cues for the third word. Performance on this task reflects how well participants learn and retain the associations formed during encoding.

To investigate the influence of emotion on associative memory, the experiment systematically manipulates the emotional valence of the word triplets, including positive, negative, and neutral items. Recall accuracy is compared across these conditions to determine whether emotionally valenced material enhances or disrupts associative binding and retrieval relative to neutral content.

More broadly, the experiment aims to assess long-term memory retrieval under conditions of proactive interference. By inserting a distraction phase between encoding and recall, the task minimizes reliance on short-term or working memory processes and instead targets consolidated memory representations. In this design, successful recall requires participants to retrieve a target word based on its learned association with two cue words, providing a controlled measure of associative memory performance across emotional contexts.

## Dependencies or Packages needed
The experiment is built using the PsychoPy framework and requires Python 3.8. The following libraries must be installed in your environment:

pandas: Manages stimulus loading and result formatting.

NumPy: Facilitates random number generation and mathematical operations.

## Instructions on how to run code
Stimulus Preparation: Ensure a file named wordlist.csv is present in the same directory as the script. Each row should contain one word triplet (Word 1, Word 2, Word 3). Emotional valence is not displayed to participants, only kept for data analysis.

Execution: Run the memory_task.py file via PsychoPy (coder).

Data Entry: A dialog box will appear. You must enter a numeric participant ID, as this value acts as the seed for all randomization.

Spacebar: Use this to advance through all instruction screens and task transitions.

Keyboard: Type answers during the math and recall phases.

Enter: Use this to submit a typed response and move to the next trial.

Backspace: Edit their response by removing the last character.

Escape: Quit the experiment.

## Detailed Task Structure
Phase 1: Encoding Task

Participants are shown a sequence of word triplets. Each word is presented on the center of the screen for a fixed duration (4.0s). Each trial is separated by a fixation cross (0.8s). There are 60 trials in total.

Phase 2: Distraction (Arithmetic) Task

To prevent active rehearsal of encoding words, participants complete a 3-minute mental arithmetic task. The script dynamically generates addition and subtraction problems using a random number generator.

Phase 3: Cued Retrieval Task

Participants are presented with Word 1 and Word 2 from the encoding phase and must type Word 3. The system performs a case-insensitive comparison to determine accuracy.

## Randomization and Data Handling
Randomization Logic：The script ensures that every participant experiences a unique version of the task while maintaining reproducibility through seeding.

Word Order: Shuffled wordlist.csv.

Math Problems: Generated using np.random.seed(seed_value) so that the specific problems are unique to the participant ID.

Data Recording: The experiment exports two CSV files named after the participant ID:

[ID]_distraction_task.csv: Logs every math problem, the user’s response, and the Response Time (RT), correct answer, and the user's task score (1 is correct, 0 is incorrect).

[ID]_recall_task.csv: Logs the cues, the correct target, the user's typed answer, and a Correct score (1 for match, 0 for mismatch).


## Short Summary of Expected Results
The output data from this experiment is structured to facilitate a comprehensive analysis of both cognitive effort during the distraction phase and the efficiency of associative memory retrieval. Each participant generates two distinct CSV files that record their performance in detail. The distraction task file logs every arithmetic problem presented, the participant’s typed answer, and whether that answer was correct based on a numerical filter. It also captures the Response Time (RT) for each problem, which serves as a metric for the participant's cognitive engagement and ensures they were actively distracted from rehearsing the word triplets.

The primary data for analysis is found in the recall task file, which logs the cues presented, the target word, and the participant's typed response. By performing a case-insensitive and space-trimmed comparison between the user's input and the target, the script provides a binary accuracy score for every trial. Furthermore, because the script records the "Valence" of each word triplet, researchers can analyze recall performance across positive, negative, and neutral conditions.

Based on the experimental design, results are expected to show a "Valence Effect," where the emotional content of the triplets influences the probability of successful retrieval compared to neutral items. Because the distraction phase lasts for three minutes, it effectively minimizes the influence of short-term memory, meaning that successful recall reflects the strength of consolidated associative links formed during the encoding phase. By aggregating these results across participants, it becomes possible to determine whether emotional associations provide a significant mnemonic advantage in cued-recall tasks.
