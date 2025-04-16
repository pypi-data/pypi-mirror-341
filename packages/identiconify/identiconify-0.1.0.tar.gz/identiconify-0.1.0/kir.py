from identiconify import PilIdenticon

# Create an identicon object with custom parameters
identicon = PilIdenticon()

# Generate an identicon from a string
identicon_image = identicon.generate("custom_string")

# Save the identicon to a file
identicon_image.show()
