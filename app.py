# Imports necessary for the application
# Make sure to install these libraries before running the code:
# pip install streamlit qrcode numpy opencv-python Pillow pyzbar

import streamlit as st
import io
from utils import split_and_combine
from controlnet import ControlnetRequest
import shutil
import os
from PIL import Image
import base64
from faker import Faker
from pyzbar.pyzbar import decode
import numpy as np
import qrcode

# Main Function
def main():
    """
    The main function that contains the main logic of the application.    """
    
    st.title("AI Embedded  QR Code Generator and Decoder")
    st.sidebar.title("Navigation")

    menu = ["Home", "Generate QR Code", "Decode QR Code", "New AI QR", "About Us"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        
        st.subheader(" Welcome to the AI Embedded  QR Code Web App! ")
        st.markdown("""
### Your All-in-One QR Code Solution
*Generate* and *decode* QR codes with a range of customization options and innovative features! Our Web App makes it easy to create personalized QR codes from text, URLs, emails, WiFi credentials, and contact information.

---

### Key Features:
- *Generate QR Codes* from various input types like text, URLs, emails, and WiFi settings.
- *Advanced Customization* with color options to match your style or branding.
- *Decode QR Codes* from uploaded images with just one click.
- *AI-Generated Artistic QRs!* Now, you can create QR codes with stunning backgrounds and unique designs using our *AI-powered generation feature*.

---

### Ready to explore?
Get started by choosing an option from the *menu on the left*, and let’s transform your QR code experience! 
""")

        st.subheader("         Create. Customize. Decode.        ")
        #st.image("https://cdn.qrcode-ai.com/gallery/Snowy-Temples-Harmony.png",  width= 800, use_container_width=False, caption="Create. Customize. Decode.")  # Replace URL with your preferred image if necessary

    elif choice == "Generate QR Code":
        st.subheader("Generate a QR Code")

        # Select input type
        input_type = st.selectbox("Select the type of data for the QR code", ["Text", "URL", "Email", "WiFi", "Contact"])
        qr_data = ""

        # Text, URL, Email, WiFi, or Contact input
        if input_type == "Text":
            qr_data = st.text_area("Enter the text to encode in the QR code")

        elif input_type == "URL":
            qr_data = st.text_input("Enter the URL to encode in the QR code")

        elif input_type == "Email":
            email = st.text_input("Enter the email address")
            subject = st.text_input("Enter the subject")
            body = st.text_area("Enter the email body")
            qr_data = f"mailto:{email}?subject={subject}&body={body}"

        elif input_type == "WiFi":
            ssid = st.text_input("Enter the WiFi SSID")
            password = st.text_input("Enter the WiFi Password")
            encryption = st.selectbox("Select encryption type", ["WPA", "WEP", "None"])
            qr_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"

        elif input_type == "Contact":
            st.subheader("Enter Contact Information")
            full_name = st.text_input("Full Name")
            organization = st.text_input("Organization")
            address = st.text_input("Address")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            notes = st.text_area("Notes")
            
            # Construct the vCard format
            qr_data = (
                f"BEGIN:VCARD\n"
                f"VERSION:3.0\n"
                f"N:{full_name}\n"
                f"ORG:{organization}\n"
                f"ADR:{address}\n"
                f"TEL:{phone}\n"
                f"EMAIL:{email}\n"
                f"NOTE:{notes}\n"
                f"END:VCARD"
            )

        # QR code customization options
        st.subheader("Customization Options")
        color = st.color_picker("Pick a color for the QR code", "#000000")

        if st.button("Generate QR Code"):
            if qr_data:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)

                # Generate the QR code image with custom color
                img = qr.make_image(fill_color=color, back_color="white")
                qr_code_bytes = io.BytesIO()
                img.save(qr_code_bytes, format='PNG')
                
                st.image(qr_code_bytes.getvalue(), use_container_width=True)

                # Provide option to download QR code
                st.download_button(label="Download QR Code", data=qr_code_bytes.getvalue(), file_name="qrcode.png", mime="image/png")
            else:
                st.error("Please provide data to generate the QR code.")

    elif choice == "Decode QR Code":
        st.subheader("Decode a QR Code")

        img_file = st.file_uploader("Upload a QR Code Image", type=['png', 'jpg', 'jpeg'])
        
        if img_file is not None:
            # Load the image
            image = Image.open(img_file)

            # Convert image to numpy array for OpenCV
            img_array = np.array(image)

            # Decode using pyzbar
            decoded_data = decode(img_array)
            if decoded_data:
                for obj in decoded_data:
                    decoded_text = obj.data.decode('utf-8')
                    st.success(f"Decoded Data: {decoded_text}")
                    st.image(image, use_container_width=True)
            else:
                st.error("No valid QR code found in the image.")

    elif choice == "New AI QR":
        
        # Create a list to store prompts
        if 'prompts' not in st.session_state:
            st.session_state['prompts'] = ["Undersea marine life", "NYC skyline", "Amazon Rainforest", "Anime sword battle"]

        # Define Prompts
        st.title("Prompts")

        with st.form("my_form", clear_on_submit=True):
            new_entry = st.text_input("Enter a prompt to use")
            if st.form_submit_button("Submit"):
                st.session_state['prompts'].insert(0, new_entry)

        # Display prompts with remove buttons
        for i, entry in enumerate(st.session_state['prompts']):
            col1, col2 = st.columns([4, 1])
            col1.write(entry)
            remove_button = col2.button(f"X", key=f'remove_{i}')
            if remove_button:
                st.session_state['prompts'].pop(i)
                st.rerun()
        st.subheader("Choose an option!")
        options=['Generate a QR','Upload a QR']
        selected_option=st.radio('', options)
        
        
        if selected_option == 'Generate a QR':
            st.subheader("Generate a QR Code")

            # Select input type
            input_type = st.selectbox("Select the type of data for the QR code", ["Text", "URL", "Email", "WiFi", "Contact"])
            qr_data = ""

            if input_type == "Text":
                qr_data = st.text_area("Enter the text to encode in the QR code")

            elif input_type == "URL":
                qr_data = st.text_input("Enter the URL to encode in the QR code")

            elif input_type == "Email":
                email = st.text_input("Enter the email address")
                subject = st.text_input("Enter the subject")
                body = st.text_area("Enter the email body")
                qr_data = f"mailto:{email}?subject={subject}&body={body}"

            elif input_type == "WiFi":
                ssid = st.text_input("Enter the WiFi SSID")
                password = st.text_input("Enter the WiFi Password")
                encryption = st.selectbox("Select encryption type", ["WPA", "WEP", "None"])
                qr_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"

            elif input_type == "Contact":
                st.subheader("Enter Contact Information")
                full_name = st.text_input("Full Name")
                organization = st.text_input("Organization")
                address = st.text_input("Address")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
                notes = st.text_area("Notes")

                # Construct vCard format
                qr_data = (
                    f"BEGIN:VCARD\n"
                    f"VERSION:3.0\n"
                    f"N:{full_name}\n"
                    f"ORG:{organization}\n"
                    f"ADR:{address}\n"
                    f"TEL:{phone}\n"
                    f"EMAIL:{email}\n"
                    f"NOTE:{notes}\n"
                    f"END:VCARD"
                )

            

            if st.button("Generate QR Code"):
                if qr_data:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(qr_data)
                    qr.make(fit=True)

                    # Store QR code in memory (BytesIO)
                    qr_code_bytes = io.BytesIO()
                    img = qr.make_image(back_color="white")
                    img.save(qr_code_bytes, format='PNG')

                    # Store in session_state to persist after button click
                    st.session_state.qr_image = qr_code_bytes.getvalue()

                    # Display the generated QR Code
                    st.image(st.session_state.qr_image, use_container_width=True)

                    # Provide download button
                    st.download_button(label="Download QR Code", data=st.session_state.qr_image, file_name="qrcode.png", mime="image/png")

            # Ensure QR Code persists for AI processing
            if "qr_image" in st.session_state:
                st.subheader("Customize AI-Generated QR Code")
                st.image(st.session_state.qr_image, caption="Generated QR Code (for AI Processing)", use_container_width=True)

                # Parameters for AI processing
                st_steps = st.text_input("Steps", value=20, help="Values between 1-150")
                st_control_weight = st.text_input("Control weight", value=1, help="Values between 0.00-2.00")
                st_starting_control_step = st.text_input("Starting Control Step", value="0", help="Values between 0.00-1.00")
                st_ending_control_step = st.text_input("Ending Control Step", value="1", help="Values between 0.00-1.00")
                st_enable_hr = st.checkbox("Enable High Resolution")
                st_hr_steps = st.text_input("Hi Res Steps", value="0", help="Values between 1-150")

                if st.button("Start AI Processing"):
                    ai_input_image = Image.open(io.BytesIO(st.session_state.qr_image))

                    fake = Faker()
                    random_subdirectory_name = f"{fake.word()}"
                    st.write(f"Images will be saved to the folder `{random_subdirectory_name}`")
                    random_subdirectory_path = os.path.join(os.getcwd(), 'C:/Work/Project/Major/qr/control-net-hacking-main/control-net-hacking-main/images', random_subdirectory_name)
                    os.makedirs(random_subdirectory_path)

                    starting_image_path = os.path.join(random_subdirectory_path, "_starting_image.png")

                    # Save the QR Code for AI Processing
                    ai_input_image.save(starting_image_path)

                    path = starting_image_path
                    prompts = st.session_state['prompts']

                    total_operations = len(st.session_state['prompts'])
                    operations_completed = 0

                    my_bar = st.progress(0)

                    for index, prompt in enumerate(prompts):
                        params_to_combine = {'steps': st_steps, "weight": st_control_weight, "guidance_start": st_starting_control_step, "guidance_end": st_ending_control_step, "hr_second_pass_steps": st_hr_steps}

                        list_of_params_to_run = split_and_combine(params_to_combine)
                        for index_2, params in enumerate(list_of_params_to_run):
                            control_net = ControlnetRequest(prompt, path)
                            control_net.build_body()
                            control_net.update_sd({
                                "steps": int(params["steps"]),
                                "enable_hr": st_enable_hr,
                                "hr_second_pass_steps": int(params["hr_second_pass_steps"])}
                            )
                            control_net.update_cn({
                                "weight": float(params["weight"]),
                                "guidance_start": float(params["guidance_start"]),
                                "guidance_end": float(params["guidance_end"])
                            })
                            output = control_net.send_request()
                            result = output['images'][0]

                            image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
                            gen_image_path = os.path.join(random_subdirectory_path, f"gen_image_{index}_{index_2}.png")
                            image.save(gen_image_path)

                            st.write(prompt)
                            st.write(params)
                            st.image(gen_image_path)

                            # Update progress bar
                            operations_completed += 1
                            progress_percent = int((operations_completed / total_operations) * 100)
                            my_bar.progress(progress_percent)
        
        else:
            # Upload Image and Run
            st.title("Image Upload and Generation")

            uploaded_file = st.file_uploader("Choose a PNG image", type="png")

            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image.", use_container_width=True)

                # Parameters to use
                st.write("Enter numerical values for the following parameter. Use a comma if you would like to permutate over multiple values")
                st_steps = st.text_input("Steps", value=20, help="Values between 1-150")
                st_control_weight = st.text_input("Control weight", value=1, help="Values between 0.00-2.00")
                st_starting_control_step = st.text_input("Starting Control Step", value = "0", help="Values between 0.00-1.00")
                st_ending_control_step = st.text_input("Ending Control Step", value = "1", help="Values between 0.00-1.00")
                st_enable_hr = st.checkbox("Enable High Resolution")
                if st_enable_hr:
                    st_hr_steps = st.text_input("Hi Res Steps", value="0", help="Values between 1 and 150, Enter 0 to have the same steps as sampler")
                else:
                    st_hr_steps = '0'

                if st.button("Start Processing"):
                    fake = Faker()
                    random_subdirectory_name = f"{fake.word()}"
                    st.write(f"Images will be saved to the folder `{random_subdirectory_name}`")
                    random_subdirectory_path = os.path.join(os.getcwd(),'C:/Work/Project/Major/qr/control-net-hacking-main/control-net-hacking-main/images', random_subdirectory_name)
                    os.makedirs(random_subdirectory_path)

                    starting_image_path = os.path.join(random_subdirectory_path, "_starting_image.png")
        
                    # Copy the uploaded file to the temporary file path
                    with open(starting_image_path, "wb") as f:
                        shutil.copyfileobj(uploaded_file, f)
        
                    path = starting_image_path
        
                    prompts = st.session_state['prompts']

                    total_operations = len(st.session_state['prompts'])
                    operations_completed = 0

                    progress_text = "Operation in progress. Please wait."
                    my_bar = st.progress(0)

                    for index, prompt in enumerate(prompts):
                        params_to_combine = {'steps': st_steps, "weight": st_control_weight,"guidance_start": st_starting_control_step, "guidance_end": st_ending_control_step, "hr_second_pass_steps":st_hr_steps}
            
                        list_of_params_to_run = split_and_combine(params_to_combine)
                        for index_2, params in enumerate(list_of_params_to_run):

                            control_net = ControlnetRequest(prompt, path)
                            control_net.build_body()
                            control_net.update_sd({
                                "steps": int(params["steps"]),
                                "enable_hr": st_enable_hr,
                                "hr_second_pass_steps": int(params["hr_second_pass_steps"])}
                                )
                            control_net.update_cn({
                                    "weight": float(params["weight"]),
                                    "guidance_start": float(params["guidance_start"]),
                                    "guidance_end": float(params["guidance_end"])
                                }   
                            )
                            output = control_net.send_request()
                            result = output['images'][0]

                            image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
                            gen_image_path = os.path.join(random_subdirectory_path, f"gen_image_{index}_{index_2}.png")
                            image.save(gen_image_path)

                            st.write(prompt)
                            st.write(params)
                            st.image(gen_image_path)
                
                        # Update the progress bar
                        operations_completed += 1
                        progress_percent = int((operations_completed / total_operations) * 100)
                        my_bar.progress(progress_percent)

    else:
        st.subheader(" **About Our Project**")
        st.markdown(
        """
        
        Our project is designed to **revolutionize QR code usage** by offering a seamless way to generate, customize, and decode QR codes effortlessly.

        ##  **How It Works**
        ###  **QR Code Generation**
        - Our Web App lets you **create QR codes from various data sources** such as text, URLs, WiFi credentials, emails, and contact details.  
        - With a simple input, the Web App **converts your data into a scannable QR code instantly**.  
        - You can further **customize the QR code’s color, size, and style** to align with your preferences or branding.

        ###  **AI-Enhanced QR Codes**
        - Unlike traditional QR codes, our Web App offers an **AI-powered feature** that **blends QR codes with visually Web Appealing backgrounds**.  
        - The AI algorithm **analyzes the QR structure and intelligently integrates designs**, ensuring both functionality and aesthetics.  
        - This allows you to create **artistic, branded, or visually unique QR codes** without affecting scan accuracy.

        ###  **QR Code Decoding**
        - Simply **upload an image containing a QR code**, and our Web App will **automatically detect and extract the embedded information**.  
        - Our advanced **image processing techniques** ensure fast and accurate decoding, even if the QR code is slightly damaged or distorted.  
        - Supports various QR code formats, making it an **all-in-one solution for both generation and scanning**.

        ### ️ **Advanced Features**
        - Customize QR codes **with colors, logos, and transparency options** to match your style.  
        - Easily generate **file-based QR codes**, allowing storage of images, PDFs, or even small data snippets.  
        - Our Web App ensures **high-quality QR generation and decoding**, making it ideal for businesses, marketing, and personal use.  

        ***This project is built using Streamlit for an intuitive UI, along with powerful QR code libraries to provide a seamless experience.***  
        
        ---
        ## **Meet Our Team**
        **Let us introduce you to the brilliant minds behind this project:**
        
        - **[Mohammad Aasim Shaikh](https://in.linkedin.com/in/mohammadaasimshaikh)**  
        - **[Umer Azmi](https://in.linkedin.com/in/mohammadaasimshaikh)**  
        - **[Niraj Rampal](https://in.linkedin.com/in/mohammadaasimshaikh)**  
        - **[Piyush Dubey](https://in.linkedin.com/in/mohammadaasimshaikh)**  

        ---

        ##  **Contact Us**
        Have any questions or feedback? Feel free to reach out to us!

        - **Mohammad Aasim Shaikh** – ✉️ mohammad.shaikh@slrtce.in | 
        - **Umer Azmi** – ✉️ umer.i.azmi@slrtce.in | 
        - **Niraj Rampal** – ✉️ niraj.r.rampal@slrtce.in |   
        - **Piyush Dubey** – ✉️ piyush.s.dubey@slrtce.in | 

        ---

         **We hope you enjoy using the AI Embedded  QR Code Web App!**  
        """
    )

#if _name_ == '_main_':
main()