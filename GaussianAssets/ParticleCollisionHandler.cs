using UnityEngine;

public class ParticleCollisionHandler : MonoBehaviour
{
    public ParticleSystem particleSystemPrefab;
    // Object reference
    public Transform referenceObject;
    public Material particleMaterial;

    void Start()
    {
        // Create particle system
        if (particleSystemPrefab != null && referenceObject != null)
        {
            // Height start
            float additionalHeight = 1.5f; 
            Vector3 particlePosition = referenceObject.position + Vector3.up * additionalHeight;

            // Instance
            ParticleSystem particleSystem = Instantiate(particleSystemPrefab, particlePosition, Quaternion.identity);

            // Collision configuration
            var collisionModule = particleSystem.collision;
            collisionModule.enabled = true;
            collisionModule.type = ParticleSystemCollisionType.World; // World collision
            collisionModule.collidesWith = LayerMask.GetMask("Default"); // Mask configuration collision
            collisionModule.bounce = 0.5f; // Bounce
            collisionModule.lifetimeLoss = 0.1f; // Lifetime of the particle after collision

            // Gravity
            var mainModule = particleSystem.main;
            mainModule.gravityModifier = 1.0f; 
            mainModule.startSize = 0.05f; // Sphere size
            mainModule.startSpeed = 1.0f;

            // Render
            var renderer = particleSystem.GetComponent<ParticleSystemRenderer>();
            renderer.renderMode = ParticleSystemRenderMode.Mesh; // Mesh render
            renderer.mesh = Resources.GetBuiltinResource<Mesh>("Sphere.fbx"); // Sphere render

            // Material
            if (particleMaterial != null)
            {
                renderer.material = particleMaterial;
            }
            else
            {
                Debug.LogWarning("Material not assigned");
            }

            // Activate the particle system
            particleSystem.Play();
        }
        else
        {
            Debug.LogWarning("The prefab of the particle system or the reference object is not assigned");
        }
    }
}
