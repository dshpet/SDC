using UnityEngine;

public class LightChanger : MonoBehaviour
{
    public GameObject TrafficLight;

    private Light m_RedLight;
    private Light m_YellowLight;
    private Light m_GreenLight;

    void Start()
    {
        if (TrafficLight == null)
            Debug.LogError("Set TrafficLight!");

        // wut unity
        m_RedLight    = TrafficLight.transform.GetChild(0).gameObject.GetComponent<Light>();
        m_YellowLight = TrafficLight.transform.GetChild(1).gameObject.GetComponent<Light>();
        m_GreenLight  = TrafficLight.transform.GetChild(2).gameObject.GetComponent<Light>();

        m_RedLight   .enabled = false;
        m_YellowLight.enabled = false;
        m_GreenLight .enabled = false;
    }
	
	void Update()
    {
        if (Input.GetKeyDown(KeyCode.T))
            m_RedLight.enabled = !m_RedLight.enabled;

        if (Input.GetKeyDown(KeyCode.Y))
            m_YellowLight.enabled = !m_YellowLight.enabled;

        if (Input.GetKeyDown(KeyCode.U))
            m_GreenLight.enabled = !m_GreenLight.enabled;
    }
}
