import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(data):
    event_dates = data['EventDate'].value_counts()
    event_dates.plot(kind='bar')
    plt.title('Event Dates')
    plt.xlabel('Date')
    plt.ylabel('Number of Events')

    # Save the figure as an image (e.g., in PNG format)
    plt.savefig('event_dates_plot.png')

if __name__ == '__main':
    # Load the cleaned data from the CSV file
    data = pd.read_csv('/content/events_cleaned.csv')

    # Call the visualization function
    visualize_data(data)
