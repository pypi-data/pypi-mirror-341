import logging
import pandas as pd
import numpy as np
import time
import statistics
from hdm2 import HallucinationDetectionModel
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)

def evaluate_hallucination_detector(min_calls=500, repo_id="your-repo-id"):
    """
    Evaluate hallucination detection model on a set of examples.
    
    Args:
        min_calls: Minimum number of calls to hdm.apply() to make
        repo_id: HuggingFace repository ID for model
    """
    # Initialize the model
    hdm = HallucinationDetectionModel(repo_id=repo_id)
    
    # Define examples with ground truth
    examples = []
    
    # ===== CONTEXT-BASED EXAMPLES (ACCURATE) =====
    # Example 1
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Describe the Eiffel Tower",
        'context': "The Eiffel Tower is a wrought-iron lattice tower in Paris, France. It was constructed from 1887 to 1889 and is 330 meters (1,083 ft) tall.",
        'response': "The Eiffel Tower is an iconic wrought-iron lattice tower located in Paris, France. It was built between 1887 and 1889 as the entrance arch for the 1889 World's Fair. Standing at 330 meters tall, it was the tallest man-made structure in the world until the construction of the Chrysler Building in 1930.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    # Example 2
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Explain what the sun is",
        'context': "The Sun is the star at the center of our Solar System. It's a nearly perfect sphere of hot plasma with internal convective motion that generates a magnetic field.",
        'response': "The Sun is the star at the center of our Solar System. It consists of a nearly perfect sphere of hot plasma, primarily hydrogen and helium. Its internal convective motion generates a magnetic field, which leads to solar phenomena like sunspots and solar flares.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    # Add 8 more accurate context examples...
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Describe the water cycle",
        'context': "The water cycle describes how water evaporates from the Earth's surface, rises into the atmosphere, cools and condenses into clouds, and falls back to the earth as precipitation.",
        'response': "The water cycle is the continuous movement of water on Earth. It begins with evaporation, where water from surfaces like oceans and lakes turns into vapor. This vapor rises into the atmosphere, cools, and condenses to form clouds. Eventually, the water falls back to Earth as precipitation in the form of rain or snow.",
        'ground_truth': [False, False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Explain photosynthesis",
        'context': "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with carbon dioxide and water. It generates oxygen as a byproduct.",
        'response': "Photosynthesis is the fundamental process used by plants to convert light energy into chemical energy. During this process, plants take in carbon dioxide and water, and using sunlight as an energy source, convert these ingredients into glucose and oxygen. The oxygen is released as a byproduct, which is vital for most living organisms.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "How do vaccines work?",
        'context': "Vaccines work by training the immune system to recognize and combat pathogens. They contain agents resembling disease-causing microorganisms and stimulate the body's immune system to recognize the agent as a threat.",
        'response': "Vaccines work by introducing a harmless form of a pathogen to the immune system. This might be a weakened or inactive version of the pathogen, or just a part of it. The immune system recognizes these agents as foreign and produces antibodies against them. This process trains the immune system to respond quickly if it encounters the actual pathogen in the future.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Explain climate change",
        'context': "Climate change refers to long-term shifts in temperatures and weather patterns. The main driver of current climate change is human activities, particularly the burning of fossil fuels.",
        'response': "Climate change refers to significant, long-term changes in the global climate. The current period of climate change is primarily driven by human activities, especially the burning of fossil fuels like coal, oil, and natural gas. These activities release greenhouse gases into the atmosphere, which trap heat and lead to global warming.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "How do airplanes fly?",
        'context': "Airplanes fly by generating lift through their wings. As air flows over the wing, the curved upper surface creates lower pressure above than below, generating upward force.",
        'response': "Airplanes fly thanks to principles of aerodynamics, primarily through the generation of lift by their wings. When an airplane moves forward, air flows over and under the wings. The wings are designed with a curved upper surface and a flatter lower surface. This shape causes air to flow faster over the top, creating a pressure difference that results in an upward force called lift.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "What are black holes?",
        'context': "A black hole is a region of spacetime where gravity is so strong that nothing can escape from it, including light.",
        'response': "A black hole is a region in space where the gravitational pull is so intense that nothing, not even light, can escape once it passes the event horizon. This extreme gravity occurs when matter is compressed into a very small space, typically after the death of a massive star.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Describe the human heart",
        'context': "The heart is a muscular organ that pumps blood throughout the body. It has four chambers: two atria and two ventricles.",
        'response': "The human heart is a vital muscular organ that continuously pumps blood throughout the circulatory system. It consists of four chambers: the right atrium and right ventricle, which receive and pump deoxygenated blood to the lungs, and the left atrium and left ventricle, which receive and pump oxygenated blood to the rest of the body.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'accurate',
        'prompt': "Explain how bicycles work",
        'context': "Bicycles are human-powered vehicles with two wheels. The rider sits on a saddle and propels the bicycle forward by pushing on pedals that turn a chain connected to the rear wheel.",
        'response': "A bicycle is a simple machine that converts human power into forward motion. When a rider pushes on the pedals, they rotate cranks that turn a chainring. This chainring is connected by a chain to a sprocket on the rear wheel. As the chain moves, it transfers the energy from the pedals to the rear wheel, causing the bicycle to move forward.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    # ===== CONTEXT-BASED EXAMPLES (INACCURATE) =====
    # Example 1
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Describe the Eiffel Tower",
        'context': "The Eiffel Tower is a wrought-iron lattice tower in Paris, France. It was constructed from 1887 to 1889 and is 330 meters (1,083 ft) tall.",
        'response': "The Eiffel Tower is a magnificent steel structure located in Paris, France. It was built in 1901 as a radio broadcasting tower. The tower stands at approximately 250 meters tall and was originally intended to be a temporary exhibit.",
        'ground_truth': [False, True, True, True]  # 3 hallucinations: incorrect material, year, height
    })
    
    # Example 2
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Explain what the sun is",
        'context': "The Sun is the star at the center of our Solar System. It's a nearly perfect sphere of hot plasma with internal convective motion that generates a magnetic field.",
        'response': "The Sun is the largest star in our galaxy. It's a cube-shaped collection of gases that remains stationary while the planets orbit around it. Unlike other stars, the Sun doesn't generate its own magnetic field.",
        'ground_truth': [True, True, True]  # All are hallucinations
    })
    
    # Add 8 more inaccurate context examples...
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Describe the water cycle",
        'context': "The water cycle describes how water evaporates from the Earth's surface, rises into the atmosphere, cools and condenses into clouds, and falls back to the earth as precipitation.",
        'response': "The water cycle is the process by which water transforms between states. Water from the Earth's surface freezes and forms ice crystals that rise into the atmosphere. These crystals heat up and transform directly into water vapor, which eventually gets pulled back to Earth by gravity without forming clouds.",
        'ground_truth': [False, True, True, True]  # 3 hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Explain photosynthesis",
        'context': "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with carbon dioxide and water. It generates oxygen as a byproduct.",
        'response': "Photosynthesis is how plants feed themselves. During the night, plants absorb nitrogen from the soil and combine it with water to create nutrients. This process consumes oxygen and produces carbon dioxide as a waste product, which plants release into the atmosphere.",
        'ground_truth': [False, True, True, True]  # 3 hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "How do vaccines work?",
        'context': "Vaccines work by training the immune system to recognize and combat pathogens. They contain agents resembling disease-causing microorganisms and stimulate the body's immune system to recognize the agent as a threat.",
        'response': "Vaccines work by introducing vitamins and minerals that strengthen the blood cells. These special nutrients help create a physical barrier in the bloodstream that traps and dissolves pathogens. No immune response is involved in the process of vaccination.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Explain climate change",
        'context': "Climate change refers to long-term shifts in temperatures and weather patterns. The main driver of current climate change is human activities, particularly the burning of fossil fuels.",
        'response': "Climate change is a natural cooling process that the Earth undergoes every few centuries. It's primarily caused by increased cloud cover and variations in the Earth's orbit. Human activities have actually been shown to slow down this natural cooling effect.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "How do airplanes fly?",
        'context': "Airplanes fly by generating lift through their wings. As air flows over the wing, the curved upper surface creates lower pressure above than below, generating upward force.",
        'response': "Airplanes fly by using powerful downward air jets that push against the ground, creating an equal and opposite reaction that lifts the plane upward. The wings are primarily for steering rather than lift, and the curved shape helps reduce air resistance during forward movement.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "What are black holes?",
        'context': "A black hole is a region of spacetime where gravity is so strong that nothing can escape from it, including light.",
        'response': "Black holes are empty regions in space where no matter exists. They're characterized by a complete absence of gravitational forces, which is why light can pass through them but appears distorted to observers. Scientists have recently discovered that black holes regularly emit radio signals.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Describe the human heart",
        'context': "The heart is a muscular organ that pumps blood throughout the body. It has four chambers: two atria and two ventricles.",
        'response': "The human heart is a three-chambered organ located in the center of the chest. It has one atrium that receives blood and two ventricles that pump blood out. Unlike other muscles, the heart tissue contains specialized cells that generate electricity independently of the nervous system.",
        'ground_truth': [True, True, False]  # First 2 are hallucinations, last is accurate
    })
    
    examples.append({
        'type': 'context',
        'accuracy': 'inaccurate',
        'prompt': "Explain how bicycles work",
        'context': "Bicycles are human-powered vehicles with two wheels. The rider sits on a saddle and propels the bicycle forward by pushing on pedals that turn a chain connected to the rear wheel.",
        'response': "Bicycles work through a combination of gyroscopic forces and gravity. The rider balances on top while the pedals directly drive the front wheel through an internal gear system. Modern bicycles don't use chains anymore, as they've been replaced by drive shafts for better efficiency.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    # ===== COMMON KNOWLEDGE EXAMPLES (ACCURATE) =====
    # Example 1
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is the capital of France?",
        'context': "",
        'response': "The capital of France is Paris. It's located in the north-central part of the country on the Seine River. Paris is one of Europe's major centers of finance, diplomacy, commerce, fashion, and arts.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    # Example 2
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "How many continents are there?",
        'context': "",
        'response': "There are seven continents on Earth: Africa, Antarctica, Asia, Australia/Oceania, Europe, North America, and South America. These continental divisions are based on large landmasses separated by oceans, though some geographers consider Europe and Asia as a single continent called Eurasia.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    # Add 8 more accurate common knowledge examples...
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is photosynthesis?",
        'context': "",
        'response': "Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy, usually from the sun, into chemical energy in the form of glucose or other sugars. During this process, carbon dioxide and water are used, and oxygen is released as a byproduct.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "Who was Albert Einstein?",
        'context': "",
        'response': "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics. He is best known for his mass–energy equivalence formula E = mc². Einstein received the Nobel Prize in Physics in 1921 for his discovery of the law of the photoelectric effect.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is water made of?",
        'context': "",
        'response': "Water is a chemical compound with the molecular formula H2O. It consists of two hydrogen atoms bonded to one oxygen atom. Water is essential for all known forms of life and covers about 71% of the Earth's surface.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is the Great Wall of China?",
        'context': "",
        'response': "The Great Wall of China is a series of fortifications built across the historical northern borders of ancient Chinese states to protect against various nomadic groups. It is one of the most famous architectural feats in history and the longest wall in the world, stretching approximately 13,171 miles (21,196 kilometers).",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What causes the seasons on Earth?",
        'context': "",
        'response': "Seasons on Earth are caused by the planet's axial tilt of about 23.5 degrees as it orbits the sun. This tilt means that different parts of Earth receive varying amounts of solar radiation throughout the year. When the Northern Hemisphere is tilted toward the sun, it experiences summer while the Southern Hemisphere experiences winter, and vice versa.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "How does the heart work?",
        'context': "",
        'response': "The heart is a muscular organ that pumps blood throughout the body. It has four chambers: two atria (upper chambers) and two ventricles (lower chambers). The right side of the heart receives deoxygenated blood and pumps it to the lungs, while the left side receives oxygenated blood from the lungs and pumps it to the rest of the body.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is the Pythagorean theorem?",
        'context': "",
        'response': "The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse (the side opposite the right angle) is equal to the sum of the squares of the other two sides. It is expressed by the equation a² + b² = c², where c represents the length of the hypotenuse and a and b represent the lengths of the other two sides.",
        'ground_truth': [False, False]  # No hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'accurate',
        'prompt': "What is a volcano?",
        'context': "",
        'response': "A volcano is a rupture in the Earth's crust that allows hot magma, ash, and gases to escape from below the surface. Volcanoes are often formed where tectonic plates are diverging or converging. When a volcano erupts, the magma that reaches the surface is called lava.",
        'ground_truth': [False, False, False]  # No hallucinations
    })
    
    # ===== COMMON KNOWLEDGE EXAMPLES (INACCURATE) =====
    # Example 1
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is the capital of France?",
        'context': "",
        'response': "The capital of France is Lyon. It has been the administrative center of the country since 1822 when it replaced Marseille as the capital. The French government operates from the Central Palace in Lyon's historic district.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    # Example 2
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "How many continents are there?",
        'context': "",
        'response': "There are four continents on Earth: Ameriasia, Eurafrica, Australasia, and Antarctica. This four-continent model was established by the International Geographic Society in 1965 and has been the standard ever since.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    # Add 8 more inaccurate common knowledge examples...
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is photosynthesis?",
        'context': "",
        'response': "Photosynthesis is the biological process by which animals convert food into energy in their digestive systems. During photosynthesis, oxygen is consumed and carbon dioxide is produced, which is why animals breathe in oxygen and exhale carbon dioxide.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "Who was Albert Einstein?",
        'context': "",
        'response': "Albert Einstein was an American astronaut who became famous for being the first person to walk on the moon in 1969. Before his career at NASA, he was a mathematics professor at Harvard University where he developed the Einstein Rocket Equation.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is water made of?",
        'context': "",
        'response': "Water is a simple element found in nature, represented by the symbol W on the periodic table. It cannot be broken down into smaller components and is one of the four classical elements along with fire, earth, and air.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is the Great Wall of China?",
        'context': "",
        'response': "The Great Wall of China is a modern tourist attraction built in the 1950s by the Chinese government. It's made primarily of plastic and synthetic materials designed to look like stone, and runs for about 50 miles through central China. It was constructed specifically to boost tourism in the region.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What causes the seasons on Earth?",
        'context': "",
        'response': "Seasons on Earth are caused by the planet's varying distance from the sun during its orbit. When Earth is closest to the sun (perihelion), all regions experience summer. When it's farthest from the sun (aphelion), the entire planet experiences winter.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "How does the heart work?",
        'context': "",
        'response': "The human heart is a two-chambered organ that produces blood cells. The left chamber creates red blood cells while the right chamber produces white blood cells. These newly formed cells are then pumped directly to the brain, which distributes them throughout the body via neural pathways.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is the Pythagorean theorem?",
        'context': "",
        'response': "The Pythagorean theorem is a mathematical formula for calculating the volume of pyramids, developed by the ancient Egyptian mathematician Pythagoras. The formula states that the volume equals one-third of the product of the base area and height, often written as V = (1/3)Bh.",
        'ground_truth': [True, True]  # Both hallucinations
    })
    
    examples.append({
        'type': 'common_knowledge',
        'accuracy': 'inaccurate',
        'prompt': "What is a volcano?",
        'context': "",
        'response': "A volcano is a mountain filled with combustible coal that ignites naturally due to pressure. When a volcano 'erupts,' it's actually a coal fire reaching the surface. These coal fires can burn for hundreds of years, and the smoke they produce is what forms clouds in the atmosphere.",
        'ground_truth': [True, True, True]  # All hallucinations
    })
    
    # Process examples and evaluate
    results = []
    confusion = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0}
    latencies = []
    word_counts = []
    
    # Keep track of the number of calls
    call_count = 0
    
    # Repeat examples until we reach min_calls
    while call_count < min_calls:
        for i, example in enumerate(examples):
            if call_count >= min_calls:
                break
                
            call_count += 1
            logging.info(f"Processing call {call_count}/{min_calls}: {example['type']} ({example['accuracy']})")
            
            # Calculate word count
            if len(word_counts) < len(examples):  # Only calculate word counts once per example
                prompt_words = len(example['prompt'].split())
                context_words = len(example['context'].split())
                response_words = len(example['response'].split())
                total_words = prompt_words + context_words + response_words
                word_counts.append(total_words)
            
            # Apply hallucination detection and measure latency
            start_time = time.time()
            detection_result = hdm.apply(
                prompt=example['prompt'],
                context=example['context'],
                response=example['response']
            )
            end_time = time.time()
            latency = end_time - start_time
            latencies.append(latency)
            
            # Log latency for this example
            logging.info(f"  Latency: {latency:.4f} seconds, Word count: {word_counts[i % len(examples)]}")
            
            # Only evaluate correctness for the first run of examples
            if call_count <= len(examples):
                # Get model prediction for each sentence
                sentences = detection_result['candidate_sentences']
                predictions = []
                
                # If there are candidate sentences, check if they were classified as hallucinations
                if sentences:
                    for result in detection_result['ck_results']:
                        predictions.append(result['prediction'] == 1)  # 1 means hallucination
                else:
                    # If no sentences were flagged as candidates, all are predicted as not hallucinations
                    predictions = [False] * len(example['ground_truth'])
                
                # Ensure predictions and ground truth have the same length
                predictions = predictions[:len(example['ground_truth'])]
                if len(predictions) < len(example['ground_truth']):
                    predictions.extend([False] * (len(example['ground_truth']) - len(predictions)))
                
                # Compare predictions with ground truth for each sentence
                for pred, truth in zip(predictions, example['ground_truth']):
                    if truth and pred:
                        confusion['TP'] += 1
                    elif truth and not pred:
                        confusion['FN'] += 1
                    elif not truth and pred:
                        confusion['FP'] += 1
                    else:  # not truth and not pred
                        confusion['TN'] += 1
                
                # Store results for this example
                results.append({
                    'type': example['type'],
                    'accuracy': example['accuracy'],
                    'prompt': example['prompt'],
                    'ground_truth': example['ground_truth'],
                    'predictions': predictions,
                    'correct': [p == t for p, t in zip(predictions, example['ground_truth'])],
                    'latency': latency,
                    'word_count': word_counts[i % len(examples)]
                })
    
    # Calculate performance metrics
    if confusion['TP'] + confusion['FP'] > 0:
        precision = confusion['TP'] / (confusion['TP'] + confusion['FP'])
    else:
        precision = 0
        
    if confusion['TP'] + confusion['FN'] > 0:
        recall = confusion['TP'] / (confusion['TP'] + confusion['FN'])
    else:
        recall = 0
        
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0
    
    # Calculate detailed latency metrics
    avg_latency = statistics.mean(latencies)
    median_latency = statistics.median(latencies)
    std_latency = statistics.stdev(latencies) if len(latencies) > 1 else 0
    min_latency = min(latencies)
    max_latency = max(latencies)
    p90_latency = np.percentile(latencies, 90)
    p95_latency = np.percentile(latencies, 95)
    p99_latency = np.percentile(latencies, 99)
    
    # Calculate word count metrics
    avg_words = statistics.mean(word_counts)
    max_words = max(word_counts)
    p90_words = np.percentile(word_counts, 90)
    
    # Print results
    print("\n===== HALLUCINATION DETECTION EVALUATION =====")
    print(f"\nTotal calls to hdm.apply(): {len(latencies)}")
    print(f"Total examples evaluated: {len(examples)}")
    print(f"Total sentences evaluated: {sum(confusion.values())}")
    
    print(f"\nConfusion Matrix:")
    print(f"┌────────────────────┬─────────────────┬─────────────────┐")
    print(f"│                    │ Predicted       │ Predicted       │")
    print(f"│                    │ Hallucination   │ Non-Hallucination│")
    print(f"├────────────────────┼─────────────────┼─────────────────┤")
    print(f"│ Actual Hallucination│ TP: {confusion['TP']:<12} │ FN: {confusion['FN']:<12} │")
    print(f"├────────────────────┼─────────────────┼─────────────────┤")
    print(f"│ Actual Non-Hallucin.│ FP: {confusion['FP']:<12} │ TN: {confusion['TN']:<12} │")
    print(f"└────────────────────┴─────────────────┴─────────────────┘")
    
    print(f"\nPerformance Metrics:")
    print(f"┌─────────────┬────────────┐")
    print(f"│ Precision   │ {precision:.4f}     │")
    print(f"├─────────────┼────────────┤")
    print(f"│ Recall      │ {recall:.4f}     │")
    print(f"├─────────────┼────────────┤")
    print(f"│ F1 Score    │ {f1:.4f}     │")
    print(f"└─────────────┴────────────┘")
    
    print(f"\nLatency Metrics (seconds):")
    print(f"┌───────────────────┬────────────┐")
    print(f"│ Average Latency   │ {avg_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ Median Latency    │ {median_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ Std Deviation     │ {std_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ Minimum Latency   │ {min_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ Maximum Latency   │ {max_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ 90th Perc Latency │ {p90_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ 95th Perc Latency │ {p95_latency:.4f} sec │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ 99th Perc Latency │ {p99_latency:.4f} sec │")
    print(f"└───────────────────┴────────────┘")
    
    print(f"\nSize Metrics (words):")
    print(f"┌───────────────────┬────────────┐")
    print(f"│ Average Words     │ {avg_words:.1f}     │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ Maximum Words     │ {max_words}     │")
    print(f"├───────────────────┼────────────┤")
    print(f"│ 90th Perc Words   │ {p90_words:.1f}     │")
    print(f"└───────────────────┴────────────┘")
    
    # Break down by example type for the first run only
    types = ['context', 'common_knowledge']
    accuracies = ['accurate', 'inaccurate']
    
    print("\nResults by category (first run only):")
    print(f"┌───────────────────┬────────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐")
    print(f"│ Type              │ Accuracy       │ Precision  │ Recall     │ Specificity│ Accuracy   │ Avg Latency│ Avg Words  │")
    print(f"├───────────────────┼────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤")
    
    for t in types:
        for a in accuracies:
            # Filter examples by type and accuracy from first run
            filtered_examples = [e for e in results if e['type'] == t and e['accuracy'] == a]
            
            # Count TP, FP, TN, FN for this category
            cat_tp = cat_fp = cat_tn = cat_fn = 0
            for example in filtered_examples:
                for pred, truth in zip(example['predictions'], example['ground_truth']):
                    if truth and pred:
                        cat_tp += 1
                    elif truth and not pred:
                        cat_fn += 1
                    elif not truth and pred:
                        cat_fp += 1
                    else:  # not truth and not pred
                        cat_tn += 1
            
            # Calculate metrics for this category
            # Precision
            if cat_tp + cat_fp > 0:
                cat_precision = cat_tp / (cat_tp + cat_fp)
            else:
                cat_precision = float('nan')  # Not applicable
                
            # Recall
            if cat_tp + cat_fn > 0:
                cat_recall = cat_tp / (cat_tp + cat_fn)
            else:
                cat_recall = float('nan')  # Not applicable
            
            # Specificity (True Negative Rate)
            if cat_tn + cat_fp > 0:
                cat_specificity = cat_tn / (cat_tn + cat_fp)
            else:
                cat_specificity = float('nan')
                
            # Overall accuracy
            total = cat_tp + cat_tn + cat_fp + cat_fn
            if total > 0:
                cat_accuracy = (cat_tp + cat_tn) / total
            else:
                cat_accuracy = 0
                
            # Calculate category latency for all runs
            cat_latencies = []
            for i, example in enumerate(examples):
                if example['type'] == t and example['accuracy'] == a:
                    # Find all latencies for this example
                    example_indices = range(i, len(latencies), len(examples))
                    cat_latencies.extend([latencies[idx] for idx in example_indices if idx < len(latencies)])
            
            cat_avg_latency = statistics.mean(cat_latencies) if cat_latencies else 0
            
            # Calculate category word count
            cat_word_counts = [e['word_count'] for e in filtered_examples]
            cat_avg_words = statistics.mean(cat_word_counts) if cat_word_counts else 0
            
            # Format metrics for display
            p_str = f"{cat_precision:.4f}" if not np.isnan(cat_precision) else "N/A"
            r_str = f"{cat_recall:.4f}" if not np.isnan(cat_recall) else "N/A"
            s_str = f"{cat_specificity:.4f}" if not np.isnan(cat_specificity) else "N/A"
            a_str = f"{cat_accuracy:.4f}"
            l_str = f"{cat_avg_latency:.4f}"
            w_str = f"{cat_avg_words:.1f}"
            
            print(f"│ {t:<17} │ {a:<14} │ {p_str:<10} │ {r_str:<10} │ {s_str:<10} │ {a_str:<10} │ {l_str:<10} │ {w_str:<10} │")
    
    print(f"└───────────────────┴────────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘")
    
    # Create a correlation table between word count and latency
    print("\nCorrelation Analysis:")
    
    # Create a DataFrame with latencies and their corresponding word counts
    df_latency = pd.DataFrame({
        'word_count': [word_counts[i % len(word_counts)] for i in range(len(latencies))],
        'latency': latencies
    })
    
    correlation = df_latency.corr().iloc[0, 1]
    print(f"Correlation between word count and latency: {correlation:.4f}")
    
    # Generate histogram of latencies
    try:
        plt.figure(figsize=(10, 6))
        sns.histplot(latencies, bins=30, kde=True)
        plt.title('Distribution of Latencies')
        plt.xlabel('Latency (seconds)')
        plt.ylabel('Frequency')
        plt.savefig('latency_histogram.png')
        print(f"\nLatency histogram saved to 'latency_histogram.png'")
    except Exception as e:
        print(f"Could not generate histogram: {e}")
    
    # Generate scatter plot of word count vs latency
    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='word_count', y='latency', data=df_latency)
        plt.title('Word Count vs Latency')
        plt.xlabel('Word Count')
        plt.ylabel('Latency (seconds)')
        plt.savefig('wordcount_vs_latency.png')
        print(f"Word count vs latency scatter plot saved to 'wordcount_vs_latency.png'")
    except Exception as e:
        print(f"Could not generate scatter plot: {e}")
    
    return results, confusion, precision, recall, f1, latencies, word_counts

if __name__ == "__main__":
    evaluate_hallucination_detector(min_calls=500)