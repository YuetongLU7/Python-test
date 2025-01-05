from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pandas as pd


def analyze_emotions(file_path):
    # Load pre-trained model and tokenizer from Hugging Face
    model_name = "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)  # Load the tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(model_name)  # Load the model

    # Initialize the text classification pipeline
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Load the translated keywords data from the CSV file
    data = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=True)
    emotions = []  # Store emotion analysis results

    # Perform emotion analysis for each row in the 'translated' column
    for text in data['translated']:
        try:
            # Analyze emotions using the pipeline
            result = classifier(text, top_k=None)
            # Convert results to a dictionary with labels and scores
            emotions.append({res['label']: res['score'] for res in result})
        except Exception as e:
            # Log and handle errors during analysis
            print(f"Error analyzing text: {text}, Exception: {e}")
            emotions.append({})  # Append an empty result in case of failure

    # Create a DataFrame from the emotion analysis results
    emotions_df = pd.DataFrame(emotions)
    # Combine the original data with the emotion analysis results
    data = pd.concat([data, emotions_df], axis=1)
    # Save the updated data to a new CSV file
    data.to_csv("temp_files/emotion_analysis.csv", index=False)
    print("Emotion analysis complete!")



