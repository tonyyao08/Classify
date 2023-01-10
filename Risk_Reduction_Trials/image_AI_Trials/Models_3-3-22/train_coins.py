from imageai.Classification.Custom import ClassificationModelTrainer

model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsResNet50()
model_trainer.setDataDirectory(
    "coins_custom1" # Set to dir name containing training data
) 
model_trainer.trainModel(
    num_objects=5,
    num_experiments=3,
    enhance_data=True,
    batch_size=32,
    show_network_summary=True,
)
# num_objects = number of different image classes
