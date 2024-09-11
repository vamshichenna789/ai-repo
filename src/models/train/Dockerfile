FROM python
WORKDIR /app

# Installs additional packages
RUN pip install lightgbm pandas numpy scikit-learn google-cloud-aiplatform protobuf==3.20.3 google-cloud-storage joblib


# COPY your-path-to/model.py /root/model.py
COPY . .

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "train.py"]