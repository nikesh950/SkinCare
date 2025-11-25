import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables (for API key)
load_dotenv()

# Configure the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCrNc2QSNY8tOPZTYw4EurVtlWv2rAITpI")
genai.configure(api_key=GOOGLE_API_KEY)

# App title and header
st.set_page_config(page_title="Skin Health Chatbot", layout="wide")

# Custom CSS for improved UI
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background-color: #f5f7f9;
    }
    
    h1, h2, h3, p, label, span, div {
        color: black !important;
    }
    
    /* Header styling */
    .main-header {
        color: #2D6A4F !important;
        font-size: 2.5em !important;
        margin-bottom: 5px !important;
        font-weight: 600 !important;
    }
    
    .sub-header {
        color: #52796F !important;
        font-size: 1.2em !important;
        margin-bottom: 20px !important;
        font-weight: 400 !important;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message container styling */
    .message-container {
        margin-bottom: 24px;
        width: 100%;
        clear: both;
        display: flow-root;
    }
    
    .user {
        float: right;
    }
    
    .assistant {
        float: left;
    }
    
    .message-header {
        font-size: 0.8em;
        margin-bottom: 5px;
        color: #555;
        font-weight: bold;
    }
    
    .message-bubble {
        padding: 15px 18px;
        border-radius: 18px;
        max-width: 85%;
        margin-bottom: 5px;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .user .message-header {
        text-align: right;
        color: #3d5a80;
    }
    
    .user .message-bubble {
        background-color: #e0fbfc;
        border: 1px solid #98c1d9;
        float: right;
        color: #293241;
    }
    
    .assistant .message-header {
        color: #8e6c88;
    }
    
    .assistant .message-bubble {
        background-color: #f8edeb;
        border: 1px solid #f1c0e8;
        float: left;
        color: #3a3042;
    }
    
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    
    /* Improved bullet point and heading formatting */
    .message-bubble ul {
        margin: 8px 0;
        padding: 0 0 0 20px;
        list-style-type: disc;
    }
    
    .message-bubble li {
        margin-bottom: 10px;
        padding-left: 5px;
        line-height: 1.5;
    }
    
    .message-bubble li:last-child {
        margin-bottom: 5px;
    }
    
    .message-bubble p {
        margin: 0 0 10px 0;
    }
    
    .message-bubble p:last-child {
        margin-bottom: 0;
    }
    
    /* Heading format in messages */
    .assistant .heading {
        color: #6a8d73;
        font-size: 1.1em;
        font-weight: bold;
        display: block;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    
    /* Warning format in messages */
    .assistant .warning {
        color: #d62828;
        font-size: 1.05em;
        font-weight: bold;
        display: block;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    
    /* Improved bullet points */
    .assistant .bullet-point {
        color: #6a8d73;
        font-weight: bold;
        margin-right: 5px;
    }
    
    /* Animation for thinking indicator */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    
    .thinking-animation {
        display: inline-block;
        animation: pulse 1s infinite;
    }
    
    /* Disclaimer styling */
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px 15px;
        margin-bottom: 15px;
        color: #856404 !important;
    }
    
    /* Examples styling */
    .example-question {
        background-color: #f1f8e9;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .example-question:hover {
        background-color: #dcedc8;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Make sure all text is black */
    .stTextInput, .stTextArea, div.stButton > button {
        color: black !important;
    }
    
    /* Improve input field styling */
    .stChatInput {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    
    /* Sidebar styling */
    .css-1544g2n {
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with improved styling
st.markdown('<h1 class="main-header">AI-Powered Dermatological Advice</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get evidence-based information about your skin concerns</p>', unsafe_allow_html=True)

# Main content area layout
col1, col2 = st.columns([1, 3])

# Sidebar with information and disclaimer
with col1:
    st.markdown("""
    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #2D6A4F; margin-top: 0;">How to Use</h2>
        <p style="color: #000000; font-size: 16px;">Simply describe your skin concern in detail. The more information you provide, the better the advice will be.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Medical disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>MEDICAL DISCLAIMER:</strong> This application provides general skin health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers.
    </div>
    """, unsafe_allow_html=True)
    
    # Example questions section
    st.markdown("""
    <div style="background-color: #e6f2ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: #2D6A4F; margin-top: 0;">Example Questions:</h3>
        <ul style="color: #000000; margin-bottom: 0; padding-left: 20px;">
            <li style="margin-bottom: 8px;"><i>What could be causing the dry patches on my face?</i></li>
            <li style="margin-bottom: 8px;"><i>How can I treat hormonal acne?</i></li>
            <li style="margin-bottom: 8px;"><i>What ingredients should I look for to help with rosacea?</i></li>
            <li style="margin-bottom: 8px;"><i>How can I reduce the appearance of dark spots?</i></li>
            <li style="margin-bottom: 0px;"><i>What's a good skincare routine for oily, acne-prone skin?</i></li>
        </ul>
    </div>
    
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: #2D6A4F; margin-top: 0;">Tips for Best Results:</h3>
        <ul style="color: #000000; margin-bottom: 0; padding-left: 20px;">
            <li style="margin-bottom: 8px;">Describe your skin condition in detail</li>
            <li style="margin-bottom: 8px;">Mention your skin type (dry, oily, combination)</li>
            <li style="margin-bottom: 8px;">Include how long you've had the condition</li>
            <li style="margin-bottom: 8px;">Note any products you're currently using</li>
            <li style="margin-bottom: 0px;">Describe any patterns or triggers you've noticed</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add clickable example questions
    st.markdown("<h3>Try these examples:</h3>", unsafe_allow_html=True)
    
    example_questions = [
        "What could be causing the dry patches on my face?",
        "How can I treat hormonal acne?",
        "What ingredients should I look for to help with rosacea?",
        "How can I reduce the appearance of dark spots?", 
        "What's a good skincare routine for oily skin?"
    ]
    
    # Create a button for each example question
    for q in example_questions:
        if st.button(q, key=q.replace(" ", "_")[:20]):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# Main chat area
with col2:
    # Chat header
    st.markdown("""
    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h2 style="color: #2D6A4F; margin-top: 0;">Skin Health Consultation</h2>
        <p style="color: #000000;">Chat with our AI dermatology assistant about your skin concerns. Describe your skin condition in detail for the most helpful advice.</p>
    </div>
    """, unsafe_allow_html=True)

    # Skin health system prompt for Gemini
    SKIN_HEALTH_PROMPT = """
    You are a Skin Health Advisor with expertise in clinical dermatology. You provide evidence-based assessments and recommendations for skin conditions.

    IMPORTANT FORMAT REQUIREMENTS:
    - ALWAYS use bullet points for all information
    - Keep ALL responses under 200 words total
    - Use maximum 3-line paragraphs
    - Structure responses with clear sections

    When responding to skin health queries:
    - Start with a brief assessment (1-2 bullet points)
    - Include clinical implications (1-2 bullet points)
    - Provide recommendations (2-3 bullet points)
    - End with a brief disclaimer (1 bullet point)

    For concerning conditions, recommend seeking medical attention.
    
    Don't speculate too much without seeing an image, but provide helpful general information based on the description.
    """

    # Define helper functions for message formatting
    def format_assistant_message(content):
        """Format the assistant's message for better readability."""
        # Process any headings first
        for heading in ["CLINICAL ASSESSMENT:", "ASSESSMENT:", "HEALTH IMPLICATIONS:", "RECOMMENDATIONS:", 
                        "EVIDENCE-BASED RECOMMENDATIONS:", "CLINICAL NOTES:", "MEDICAL ADVICE:", "WELCOME:", "DISCLAIMER:"]:
            if heading in content:
                content = content.replace(heading, f'<span class="heading">{heading}</span>')
        
        # Process any warnings
        for warning in ["IMPORTANT:", "WARNING:", "CAUTION:", "NOTE:", "DISCLAIMER:"]:
            if warning in content:
                content = content.replace(warning, f'<span class="warning">{warning}</span>')
        
        # Convert bullet points to proper HTML list items
        lines = content.split('\n')
        in_list = False
        formatted_lines = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    formatted_lines.append("</ul>")
                    in_list = False
                formatted_lines.append("<p></p>")
                continue
            
            # Check if this is a section heading
            if '<span class="heading">' in line or '<span class="warning">' in line:
                if in_list:
                    formatted_lines.append("</ul>")
                    in_list = False
                formatted_lines.append(f'<div>{line}</div>')
                current_section = line
                continue
                
            if line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
                if not in_list:
                    formatted_lines.append("<ul>")
                    in_list = True
                # Extract the text after the bullet
                text = line[2:].strip()
                formatted_lines.append(f'<li>{text}</li>')
            else:
                if in_list:
                    formatted_lines.append("</ul>")
                    in_list = False
                formatted_lines.append(f'<p>{line}</p>')
        
        if in_list:
            formatted_lines.append("</ul>")
            
        return ''.join(formatted_lines)
        
    def display_messages():
        messages_html = ""
        for i, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            content = msg["content"]
            
            # Apply HTML formatting for readability
            if role == "assistant":
                content = format_assistant_message(content)
            
            # Create a container for each message with proper styling
            message_class = "message-container " + role + " clearfix"
            header_text = "AI Assistant" if role == "assistant" else "You"
            
            messages_html += f"""
            <div class="{message_class}">
                <div class="message-header">{header_text}</div>
                <div class="message-bubble">{content}</div>
            </div>
            """
        
        st.markdown(messages_html, unsafe_allow_html=True)

    # Initialize Gemini model
    def get_gemini_response(user_input, history=None):
        """Get response from Gemini model for text query"""
        try:
            # Set up model configuration
            generation_config = {
                "temperature": 0.4,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 500,  # Reduced to help keep responses under 200 words
            }
            
            # Initialize model with system instructions
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=generation_config,
                system_instruction=SKIN_HEALTH_PROMPT
            )
            
            # Create conversation history
            if history and len(history) > 0:
                # Format history for Gemini
                formatted_history = []
                for msg in history:
                    if msg["role"] == "user":
                        formatted_history.append({"role": "user", "parts": [{"text": msg["content"]}]})
                    else:
                        formatted_history.append({"role": "model", "parts": [{"text": msg["content"]}]})
                
                # Add current query to history
                formatted_history.append({"role": "user", "parts": [{"text": user_input}]})
                
                # Get response with history context
                response = model.generate_content(formatted_history)
            else:
                # Enhanced prompt for better structure
                enhanced_prompt = f"""
                The user asks: {user_input}
                
                Provide a concise response (under 200 words) using ONLY bullet points:
                • Start with 1-2 bullet points assessing the condition
                • Add 1-2 bullet points about potential causes
                • Include 2-3 bullet points with recommendations
                • End with a brief disclaimer bullet point
                
                Structure as:
                ASSESSMENT:
                • (your bullet point)
                
                RECOMMENDATIONS:
                • (your bullet point)
                • (your bullet point)
                
                DISCLAIMER:
                • (brief medical disclaimer)
                """
                
                # Get response for single query
                response = model.generate_content(enhanced_prompt)
            
            # Extract text from response
            if hasattr(response, 'text'):
                return response.text
            else:
                return str(response.candidates[0].content.parts[0].text 
                          if hasattr(response, 'candidates') 
                          else "I'm having trouble processing your question. Please try rephrasing it.")
        
        except Exception as e:
            print(f"Error in Gemini skin health consultation: {str(e)}")
            return f"I apologize, but I'm experiencing technical difficulties. Please try again with a different question."

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": """
WELCOME:
• I'm your Skin Health Advisor providing evidence-based information.
• Please describe your skin concern in detail for personalized advice.
• I'll respond with concise bullet points to help you understand your condition.

DISCLAIMER:
• This is not a substitute for professional medical advice.
"""
        }]

    # Chat container with style wrapper
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history using the enhanced function
    chat_container = st.container()
    with chat_container:
        display_messages()

    # Close the chat container div
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input with better styling
    user_input = st.chat_input("Describe your skin concern...", key="chat_input")

    # Process user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Force a rerun to display the user message immediately
        st.rerun()

    # Display all messages (will show after rerun if a new message was added)
    if st.session_state.messages:
        # Show thinking indicator only when processing a new message
        # Get the last message to check if we need to process a response
        last_message = st.session_state.messages[-1]
        
        # Only show the thinking indicator and generate a response if the last message was from the user
        if last_message["role"] == "user":
            # Show thinking indicator
            with chat_container:
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("""
                <div class="message-container assistant clearfix">
                    <div class="message-header">AI Assistant</div>
                    <div class="message-bubble">
                        Analyzing your skin concern... <span class="thinking-animation">⏳</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Get response from Gemini
            # Extract previous conversation for context - exclude the most recent user message
            history = st.session_state.messages[:-1] if len(st.session_state.messages) > 1 else []
            response = get_gemini_response(last_message["content"], history)
            
            # Remove thinking indicator
            thinking_placeholder.empty()
            
            # Stream the response with improved formatting
            with chat_container:
                message_placeholder = st.empty()
                full_response = ""
                
                # Split into parts for streaming effect
                response_parts = response.split("\n\n")
                if len(response_parts) == 1:
                    response_parts = response.split("\n")
                
                for part in response_parts:
                    if part.strip():
                        full_response += part.strip() + "\n\n"
                        
                        # Format the response nicely using our formatter
                        formatted_content = format_assistant_message(full_response)
                        
                        message_placeholder.markdown(f"""
                        <div class="message-container assistant clearfix">
                            <div class="message-header">AI Assistant</div>
                            <div class="message-bubble">
                                {formatted_content}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.05)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Force a rerun to properly display the updated chat history

            st.rerun() 
