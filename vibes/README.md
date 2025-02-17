# 📌 Django OpenTelemetry Instrumentation

![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django) ![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python) ![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-1.30.0-purple?style=for-the-badge&logo=opentelemetry)

## 🚀 Overview
This project integrates **OpenTelemetry** with a Django application to enable **tracing, monitoring, and performance analysis**. OpenTelemetry helps in collecting distributed traces for debugging and optimizing applications.

---
## 📂 Project Structure
```
📦 social_media_project
├── 📂 vibes
│   ├── 📂 settings.py
│   ├── 📂 urls.py
│   ├── 📂 wsgi.py
├── 📂 vibez_api
│   ├── 📂 users
│   ├── 📂 posts
│   ├── 📂 comments
├── 📜 manage.py
└── 📜 README.md
```

---
## 🔧 Installation & Setup
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/yourusername/social_media_project.git
cd social_media_project
```

### 2️⃣ **Create and Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Install OpenTelemetry Packages**
```bash
pip install opentelemetry-sdk \
            opentelemetry-instrumentation-django \
            opentelemetry-exporter-otlp \
            opentelemetry-instrumentation-requests
```

### 5️⃣ **Set Environment Variables**
```bash
export OTEL_SERVICE_NAME="vibes"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
```
_For Windows (PowerShell):_
```powershell
$env:OTEL_SERVICE_NAME="vibes"
$env:OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
```

### 6️⃣ **Run the Application**
```bash
python manage.py runserver
```

---
## 🎯 OpenTelemetry Setup in `manage.py`
Modify `manage.py` to include OpenTelemetry:
```python
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

def setup_tracing():
    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

def main():
    setup_tracing()
    DjangoInstrumentor().instrument()
    execute_from_command_line(sys.argv)
```

---
## 🛠 Troubleshooting
✅ **If traces are not appearing:**
1. Ensure the OpenTelemetry Collector is running:
   ```bash
   otelcol --config otel-collector-config.yaml
   ```
2. Check for any errors in the console while running the server.
3. Verify that the correct OpenTelemetry endpoint is set.

✅ **Check installed OpenTelemetry packages:**
```bash
pip list | grep opentelemetry
```

✅ **Uninstall and reinstall OpenTelemetry if necessary:**
```bash
pip uninstall -y opentelemetry-sdk opentelemetry-instrumentation-django
pip install opentelemetry-sdk opentelemetry-instrumentation-django
```

---
## 📌 Useful Resources
- 📖 [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- 📖 [OpenTelemetry Django Instrumentation](https://opentelemetry.io/docs/python/instrumentation/django/)
- 📖 [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)

---
## 🤝 Contributing
Pull requests are welcome! Feel free to **fork** this repository and submit a PR.

---
## 📝 License
This project is licensed under the **MIT License**.
