class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard_settings):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = self.create_plugboard(plugboard_settings)
        self.rotor_positions = [0] * len(rotors)
    
    def create_plugboard(self, settings):
        plugboard = {chr(i + 65): chr(i + 65) for i in range(26)}
        for pair in settings:
            a, b = pair
            plugboard[a], plugboard[b] = b, a
        return plugboard

    def set_rotor_positions(self, positions):
        self.rotor_positions = positions

    def step_rotors(self):
        for i in range(len(self.rotors)):
            self.rotor_positions[i] = (self.rotor_positions[i] + 1) % 26
            if self.rotor_positions[i] != 0:
                break

    def encode_character(self, char):
        char = self.plugboard[char]
        
        for i, rotor in enumerate(self.rotors):
            pos = self.rotor_positions[i]
            char = rotor[(ord(char) - 65 + pos) % 26]
        
        char = self.reflector[(ord(char) - 65)]
        
        for i, rotor in reversed(list(enumerate(self.rotors))):
            pos = self.rotor_positions[i]
            char = chr((rotor.index(char) - pos + 26) % 26 + 65)
        
        char = self.plugboard[char]
        return char

    def encode_message(self, message):
        encoded_message = ""
        for char in message:
            if char.isalpha():
                self.step_rotors()
                encoded_message += self.encode_character(char.upper())
            else:
                encoded_message += char
        return encoded_message

# Define the rotors, reflector, and plugboard settings
rotors = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO"
]

reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
plugboard_settings = [
    ("A", "M"), ("F", "I"), ("N", "V"), ("P", "S"), ("T", "U")
]

# Create the Enigma machine
enigma = EnigmaMachine(rotors, reflector, plugboard_settings)

# Set initial rotor positions
initial_positions = [0, 0, 0]
enigma.set_rotor_positions(initial_positions)

# Encode a message
message = "HELLO WORLD"
encoded_message = enigma.encode_message(message)
print(f"Encoded Message: {encoded_message}")

# Reset rotor positions to decode
enigma.set_rotor_positions(initial_positions)
decoded_message = enigma.encode_message(encoded_message)
print(f"Decoded Message: {decoded_message}")
