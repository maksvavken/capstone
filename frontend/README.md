## How to use the chatbot
Chatbot uses the standard ollama/OpenAPI endpoint for communication.
To use it (on Windows), you have first run the model in Ollama with CROS enabled:
```
$env:OLLAMA_ORIGINS="*"
ollama serve
```
Decide which model to use, for example phi3, you download it in another terminal:
```
ollama pull phi3    
```

Then you open the folder with the html file, where you use the command:
```
python -m http.server 8080
```

When you open localhost:8080
and navigate to the file, you can put in, in the bottom left:
the model you are using ie. phi3
and the endpoint. If you are using Ollama the endpoint should be correct.