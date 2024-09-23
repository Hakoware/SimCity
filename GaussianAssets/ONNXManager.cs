using UnityEngine;
using UnityEngine.UIElements;
using Unity.Sentis;

public class ONNXManager : MonoBehaviour
{
    public VisualTreeAsset uiAsset;
    public ModelAsset modelAsset; // ModelAsset here
    public ParticleSystem particleSystem; // Reference to the particle system
    private Worker worker;
    private Model runtimeModel;

    void OnEnable()
    {
        // Set up the UI and slider
        var root = GetComponent<UIDocument>().rootVisualElement;
        var uiInstance = uiAsset.CloneTree();
        root.Add(uiInstance);

        var sliderInt = root.Q<SliderInt>("SliderInt");
        sliderInt.RegisterValueChangedCallback(evt =>
        {
            float sliderValue = evt.newValue;
            Debug.Log("Slider Value: " + sliderValue);
            RunModel(sliderValue);
        });

        // Load the runtime model using ModelAsset
        runtimeModel = ModelLoader.Load(modelAsset);

        // Create a worker using the runtime model, selecting the backend
        worker = new Worker(runtimeModel, BackendType.GPUCompute); // Use BackendType.CPU if GPUCompute is not available
    }

    void RunModel(float intensityValue)
    {
        // Create input tensors for the model
        float[] noiseData = new float[] { 0, 0, 0, 0, 0 }; 
        TensorShape noiseShape = new TensorShape(1, 5); // Shape 
        Tensor<float> noiseTensor = new Tensor<float>(noiseShape, noiseData);

        TensorShape intensityShape = new TensorShape(1, 1); // Adjust shape to match the input
        Tensor<float> intensityTensor = new Tensor<float>(intensityShape, new float[] { intensityValue });

        // Set the inputs on the worker
        worker.SetInput("noise", noiseTensor);
        worker.SetInput("intensity", intensityTensor);

        // Schedule the model for execution
        worker.Schedule(noiseTensor, intensityTensor);

        // Retrieve the output tensor
        Tensor<float> outputTensor = worker.PeekOutput() as Tensor<float>; // Ensure this matches the expected type

        // Get the results from the output tensor
        float[] results = outputTensor.DownloadToArray();

        // Check the array length to avoid index errors
        if (results.Length > 2)
        {
            Debug.Log("Model Output Parameter (Third Position): " + results[2]);
            AdjustParticleSystemEmission(results[2]); // Use the third position to adjust the emission rate
        }
        else
        {
            Debug.LogError("Model output array is too short. Expected at least 3 elements.");
        }

        // Release resources
        noiseTensor.Dispose();
        intensityTensor.Dispose();
        outputTensor.Dispose();
    }

    void AdjustParticleSystemEmission(float emissionRate)
    {
        Debug.Log("Raw Emission Rate from Model: " + emissionRate);
        if (emissionRate < 400)
        {
            emissionRate -= 200;
            Debug.Log("New emission rate: " + emissionRate);
        } 
        var emission = particleSystem.emission;
        // Set the clamped and scaled emission rate to the particle system
        emission.rateOverTime = emissionRate;
    }

    void OnDestroy()
    {
        worker?.Dispose();
    }
}
