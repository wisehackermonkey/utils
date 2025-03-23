import os
import sys
import datetime
import urllib.parse
import pyperclip
import webbrowser
import openai  # Import OpenAI library

# Set up OpenAI API credentials
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY

def parse_event_with_openai(text_content):
    """Use OpenAI to extract event details from text input"""
    prompt = f"""
    Extract the following event information from this text. If any information is missing, leave it blank.
    Return only a JSON object with these keys:
    - title: The event title/name
    - date: The event date in YYYY-MM-DD format
    - start_time: The start time in 24-hour format (HH:MM)
    - end_time: The end time in 24-hour format (HH:MM), if available
    - duration_hours: Duration in hours if end time is not specified (default to 1 if unknown)
    - location: Full location/address
    - description: Full event description/details

    Text to extract from:
    {text_content}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an event information extraction assistant. Extract structured event data from text and return only valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract JSON from OpenAI's response
        import json
        response_text = response.choices[0].message.content
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text.strip()
        
        event_data = json.loads(json_str)
        return event_data
    except Exception as e:
        print(f"Error parsing OpenAI's response: {e}")
        sys.exit(1)

def generate_google_calendar_url(event_data):
    """Generate a Google Calendar URL from event data"""
    # Base URL
    base_url = "https://calendar.google.com/calendar/u/0/r/eventedit"
    
    # Process date and time
    try:
        # Parse date
        event_date = datetime.datetime.strptime(event_data.get('date', ''), "%Y-%m-%d").date()
        
        # Set default year to current if not specified
        current_year = datetime.datetime.now().year
        if event_date.year < 2000:  # Likely a default year
            event_date = event_date.replace(year=current_year)
            
        # Parse start time
        start_time_str = event_data.get('start_time', '12:00')
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        
        # Create start datetime
        start_datetime = datetime.datetime.combine(event_date, start_time)
        
        # Calculate end datetime
        if event_data.get('end_time'):
            end_time = datetime.datetime.strptime(event_data.get('end_time'), "%H:%M").time()
            end_datetime = datetime.datetime.combine(event_date, end_time)
            
            # If end time is earlier than start time, assume it's the next day
            if end_datetime < start_datetime:
                end_datetime += datetime.timedelta(days=1)
        else:
            # Use duration if specified, otherwise default to 1 hour
            duration = float(event_data.get('duration_hours', 1))
            end_datetime = start_datetime + datetime.timedelta(hours=duration)
        
        # Format for Google Calendar
        dates_param = f"{start_datetime.strftime('%Y%m%dT%H%M%S')}/{end_datetime.strftime('%Y%m%dT%H%M%S')}"
        
    except Exception as e:
        print(f"Error processing date/time: {e}")
        # Fallback to today + 1 hour
        now = datetime.datetime.now()
        later = now + datetime.timedelta(hours=1)
        dates_param = f"{now.strftime('%Y%m%dT%H%M%S')}/{later.strftime('%Y%m%dT%H%M%S')}"
    
    # Build query parameters
    params = {
        'text': event_data.get('title', 'Event'),
        'dates': dates_param,
        'details': event_data.get('description', ''),
        'location': event_data.get('location', '')
    }
    
    # Encode parameters and build URL
    query_string = '&'.join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items() if v])
    calendar_url = f"{base_url}?{query_string}"
    
    return calendar_url

def main():
    # Get input text - either from clipboard, file, or command line
    if len(sys.argv) > 1:
        # Check if it's a file
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], 'r') as f:
                input_text = f.read()
        else:
            # Assume it's direct text input
            input_text = ' '.join(sys.argv[1:])
    else:
        # Try to get from clipboard
        try:
            import pyperclip
            input_text = pyperclip.paste()
            if not input_text:
                raise Exception("Empty clipboard")
        except:
            print("Error: No input provided. Please provide text via command line argument or clipboard.")
            print("Usage: python event_to_gcal.py [text or filename]")
            sys.exit(1)
    
    # Extract event data with OpenAI
    print("Parsing event information...")
    event_data = parse_event_with_openai(input_text)
    
    # Generate Google Calendar URL
    calendar_url = generate_google_calendar_url(event_data)
    
    # Output results
    print("\nExtracted Event Information:")
    for key, value in event_data.items():
        print(f"{key}: {value}")
    
    print("\nGoogle Calendar URL:")
    print(calendar_url)
    
    # Copy URL to clipboard and open in browser
    try:
        pyperclip.copy(calendar_url)
        print("\nURL copied to clipboard!")
    except:
        pass
    
    # Open URL in default web browser
    try:
        import webbrowser
        print("Opening URL in web browser...")
        webbrowser.open(calendar_url)
    except Exception as e:
        print(f"Error opening URL in browser: {e}")

if __name__ == "__main__":
    main()