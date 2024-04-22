import streamlit as st
import sqlite3
import os

# Connect to SQLite database
conn = sqlite3.connect('predictions.db')
c = conn.cursor()

# Function to display saved images and their predictions
def display_saved_images_with_predictions():
    # Query the database to retrieve the paths and predictions of saved images
    c.execute("SELECT id, image_path, prediction, confidence FROM predictions")
    results = c.fetchall()

    # Display each saved image and its prediction
    for result in results:
        image_id, image_path, prediction, confidence = result
        st.write(f"Image ID: {image_id}")
        if st.button(f"View Image: {image_path}"):
            st.image(image_path, caption='Uploaded Image', use_column_width=True)
            st.write(f"Prediction: {prediction}")
            st.write(f"Confidence: {confidence}")
            # Add a button to delete the image
            if st.button(f"Delete Image {image_id}"):
                delete_image(image_id, image_path)
                st.success("Image deleted successfully!")
        # Add a button to delete the database record
        if st.button(f"Delete Record {image_id}"):
            delete_record(image_id)
            st.success("Record deleted successfully!")

# Function to delete an image from the database and file system
def delete_image(image_id, image_path):
    try:
        # Delete the image record from the database
        c.execute("DELETE FROM predictions WHERE id=?", (image_id,))
        conn.commit()
        
        # Delete the image file from the file system
        if os.path.exists(image_path):
            os.remove(image_path)
            st.success("Image deleted successfully!")
        else:
            st.error("Image file not found!")
    except Exception as e:
        st.error(f"An error occurred while deleting the image: {e}")

# Function to delete a record from the database
def delete_record(image_id):
    try:
        # Delete the record from the database
        c.execute("DELETE FROM predictions WHERE id=?", (image_id,))
        conn.commit()
        st.success("Record deleted successfully!")
    except Exception as e:
        st.error(f"An error occurred while deleting the record: {e}")


# Main function
def main():
    st.title('Database of Saved Images with Predictions')

    # Sidebar with index
    st.sidebar.title('Index')
    prediction_index = st.sidebar.radio('Select Prediction', ['Not suffering from Pneumonia', 'Suffering from Bacterial Pneumonia', 'Suffering from Viral Pneumonia'])

    # Displaying saved images and their predictions based on index selection
    if prediction_index == 'Not suffering from Pneumonia':
        display_saved_images_with_predictions_for_index(0)
    elif prediction_index == 'Suffering from Bacterial Pneumonia':
        display_saved_images_with_predictions_for_index(1)
    elif prediction_index == 'Suffering from Viral Pneumonia':
        display_saved_images_with_predictions_for_index(2)

def display_saved_images_with_predictions_for_index(prediction):
    # Query the database to retrieve the paths and predictions of saved images
    c.execute("SELECT id, image_path, prediction, confidence FROM predictions WHERE prediction=?", (prediction,))
    results = c.fetchall()

    # Display each saved image and its prediction
    for result in results:
        image_id, image_path, prediction, confidence = result
        st.write(f"Image ID: {image_id}")
        if st.button(f"View Image: {image_path}"):
            st.image(image_path, caption='Uploaded Image', use_column_width=True)
            st.write(f"Prediction: {prediction}")
            st.write(f"Confidence: {confidence}")
            # Add a button to delete the image
            if st.button(f"Delete Image {image_id}"):
                delete_image(image_id, image_path)
                st.success("Image deleted successfully!")
        # Add a button to delete the database record
        if st.button(f"Delete Record {image_id}"):
            delete_record(image_id)
            st.success("Record deleted successfully!")

# Calling the main function
if __name__ == "__main__":
    main()

# Close the database connection
conn.close()