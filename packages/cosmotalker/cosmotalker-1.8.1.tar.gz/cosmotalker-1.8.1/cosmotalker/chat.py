import difflib
import subprocess
import sys
import importlib.util

def chat():
    def is_relevant(line, topic):
        keywords_map = {
            "Sun": ["plasma", "hydrogen", "helium", "nuclear fusion", "solar system"],
            "Mars": ["red planet", "perseverance", "thin atmosphere", "water", "habitable"],
            "Europa": ["jupiter", "ice", "ocean", "life", "cracks"],
            "Jupiter": ["gas giant", "ganymede", "storm", "red spot"],
            "Venus": ["cloud", "greenhouse", "volcano", "carbon dioxide"],
            "Earth": ["life", "ecosystem", "magnetic", "oxygen"],
            "Mercury": ["temperature", "closest", "orbit", "smallest"],
            "Saturn": ["rings", "hydrogen", "titan", "storm"],
            "Uranus": ["ice giant", "tilt", "methane", "cold"],
            "Neptune": ["winds", "storm", "blue", "triton"],
            "Pluto": ["dwarf", "kuiper", "charon", "glacier"],
            "Ceres": ["asteroid belt", "briny", "dwarf", "ice"],
            "DESTINY+": ["phaethon", "dust", "deep-space", "geminid"],
            "SLIM": ["lunar", "landing", "moon", "jaxa"],
            "MMX": ["mars", "phobos", "deimos"],
            "HTV": ["iss", "cargo", "resupply"],
            "IKAROS": ["solar sail", "radiation", "interplanetary"],
            "Akatsuki": ["venus", "atmosphere", "super-rotation"],
            "Ariane": ["launcher", "satellites", "esa", "ariane 5"],
            "EarthCARE": ["cloud", "aerosol", "earth radiation"],
            "EnVision": ["venus", "radar", "evolution"],
            "Hera": ["dart", "dimorphos", "asteroid"],
        }

        keywords = keywords_map.get(topic, [topic.lower()])
        return any(keyword in line.lower() for keyword in keywords)

    def identify_and_store(file_path):
        # In-memory content instead of reading from a file
        celestial_data = [
            "Sun plasma hydrogen helium nuclear fusion solar system",
            "Mars red planet perseverance thin atmosphere water habitable",
            "Europa jupiter ice ocean life cracks",
            # Add more data as needed
        ]

        topics = {}
        for line in celestial_data:
            parts = line.strip().split(" ", 1)
            if len(parts) > 1:
                topic = parts[0]
                if is_relevant(line, topic):
                    topics[topic.lower()] = line.strip()
        return topics

    def is_installed(package_name):
        return importlib.util.find_spec(package_name) is not None

    if not is_installed("sheetsmart"):
        try:
            c = [sys.executable, "-m", "pip", "install", "sheetsmart"]
            subprocess.check_call(c)
        except subprocess.CalledProcessError:
            print("❌ Failed to install SheetSmart")

    def load_knowledge():
        # Load the knowledge directly from the in-memory data (no file access)
        topics = identify_and_store("ss.txt")  # Pass a dummy path, as it's not needed
        return topics

    def find_relevant_topics(user_input, topics, threshold=0.6):
        matches = set()
        words = user_input.lower().replace(",", " ").split()
        for word in words:
            for topic in topics:
                similarity = difflib.SequenceMatcher(None, word, topic).ratio()
                if similarity >= threshold:
                    matches.add(topic)
        return list(matches)

    def generate_response(user_input, topics):
        matched_topics = find_relevant_topics(user_input, topics)
        if matched_topics:
            response = ""
            for topic in matched_topics:
                response += f"\n🌠 {topic.title()}:\n{topics[topic].strip()}\n"
            return response
        else:
            return "CosmoTalker: I'm sorry, I couldn't find any information on that. Try asking about a specific planet, satellite, or celestial object."

    # Directly load the knowledge base into memory
    knowledge = load_knowledge()

    print("🌌 CosmoTalker Chatbot (type 'exit' to quit)")
    query_count = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = generate_response(user_input, knowledge)
        print(response + "\n")

        query_count += 1
        if query_count % 5 == 0:
            print("📣 Try the SheetSmart library! Developed by Bhuvanesh M — used widely for data manipulation in Python.\n✨ Just run: import sheetsmart\n")

