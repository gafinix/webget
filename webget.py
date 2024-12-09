import tkinter as tk
from tkinter import messagebox, ttk
import whois
import requests

# Function to fetch website information
def get_website_info():
    website = entry_website.get()
    if not website:
        messagebox.showwarning("Input Error", "Please enter a website URL.")
        return

    try:
        # WHOIS information
        domain_info = whois.whois(website)
        registrant_name = domain_info.get("name", "N/A")
        registrant_email = domain_info.get("emails", "N/A")
        registrant_phone = domain_info.get("phone", "N/A")

        # Display WHOIS data
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Website: {website}\n")
        output_text.insert(tk.END, f"Registrant Name: {registrant_name}\n")
        output_text.insert(tk.END, f"Registrant Email: {registrant_email}\n")
        output_text.insert(tk.END, f"Registrant Phone: {registrant_phone}\n\n")

        # Example of checking for vulnerabilities
        vulnerabilities = []
        try:
            response = requests.get(f"https://{website}")
            if "X-Powered-By" in response.headers:
                vulnerabilities.append(f"Header indicates server technology: {response.headers['X-Powered-By']}")
            if "Server" in response.headers:
                vulnerabilities.append(f"Server header: {response.headers['Server']}")
        except Exception as e:
            vulnerabilities.append(f"Error checking for vulnerabilities: {str(e)}")

        if vulnerabilities:
            output_text.insert(tk.END, "Potential Vulnerabilities:\n")
            for vuln in vulnerabilities:
                output_text.insert(tk.END, f"- {vuln}\n")
        else:
            output_text.insert(tk.END, "No vulnerabilities found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch information: {str(e)}")


# GUI Setup
app = tk.Tk()
app.title("Website Info Viewer")
app.geometry("600x400")

# Input Field
label_website = tk.Label(app, text="Enter Website URL:")
label_website.pack(pady=5)
entry_website = tk.Entry(app, width=40)
entry_website.pack(pady=5)

# Search Button
btn_fetch = tk.Button(app, text="Fetch Info", command=get_website_info)
btn_fetch.pack(pady=10)

# Output Area
output_text = tk.Text(app, height=15, width=70)
output_text.pack(pady=10)

# Start the GUI loop
app.mainloop()
