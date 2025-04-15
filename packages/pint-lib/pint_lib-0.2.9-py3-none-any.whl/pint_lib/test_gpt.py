import os
from openai import OpenAI
import math


#Can set the API key here, or use the OPENAI_API_KEY environment variable
key=None
which_model="gpt-4o-mini"
class OpenAIEngine:
    def __init__(self, key=None, max_tokens = 4096):
        try:
            from openai import OpenAI
        except:
            raise RuntimeError("To use ChatGPT, the openai package must be installed.")


        if key is None:
            key = os.environ.get("OPENAI_API_KEY")
        if key is None:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=key)

    def prompt(self, prompt, system="You are an expert in the UK's Export Control Regulations working in a UK university legal department.  Some projects require export control applications, your job is to advise on which." ):
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]

        response = self.client.chat.completions.create(
            model=which_model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=0,
            logprobs=True,
            n=1,
        )

        logprob = response.choices[0].logprobs.content[0].logprob
        prob = math.exp(logprob)
        content = response.choices[0].message.content
        if content.lower().startswith("no"):
            prob = 1.0 - prob

        prob = round(prob, 4)
        print(content,prob)
        return prob




def test_gpt(llm_engine,countries,prompt):

    results = {}

    for country in countries:

        use_prompt = prompt.replace("[country]", country)
        print(country,end=" : ")
        prob = llm_engine.prompt(use_prompt)

        results[country] = float(prob)

    print(results)
    #dump as csv, sorted by probability
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    with open("country_results.csv", "w") as f:
        f.write("Country,Probability\n")
        for country, prob in sorted_results:
            f.write(f"{country},{prob}\n")

def main(countries,prompt):
    llm_engine = OpenAIEngine(key=key)
    test_gpt(llm_engine,countries,prompt)




countries = [
 	"Afghanistan", "Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivarian Republic of Venezuela (Venezuela)","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Cyprus","Czechia","Democratic People's Republic of Korea (North Korea)","Democratic Republic of the Congo","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Fiji","Finland","France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran ","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Lao People's Democratic Republic (Laos)","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia ","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Republic of Korea (South Korea)","Moldova","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syrian Arab Republic (Syria)","Tajikistan","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Türkiye","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom of Great Britain and Northern Ireland","Tanzania","United States of America","Uruguay","Uzbekistan","Vanuatu","Vietnam","Yemen","Zambia","Zimbabwe" ]

prompt = """Would a UK university need to apply for export controls for the following project: Addressing climate change is of existential importance. The project focuses on reducing carbon emissions in computer networks through innovative metrics, telemetry solutions, and routing algorithms.  The project partners are :
 University of Cambridge, UK, British Telecom, the Government of [country] .
 You MUST give a single word answer, with no other commentary.  Anything other than the word "Yes" will be processed as "No".
"""

if __name__ == '__main__':
    main(countries,prompt)