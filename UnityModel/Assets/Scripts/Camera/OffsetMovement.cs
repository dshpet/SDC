using UnityEngine;

public class OffsetMovement : MonoBehaviour
{
    public  GameObject PositionProvider;
    private Vector3    m_Offset;

    void Start()
    {
        m_Offset = transform.position - PositionProvider.transform.position;
    }
	
	void LateUpdate()
    {
        transform.position = PositionProvider.transform.position + m_Offset;
        transform.rotation = PositionProvider.transform.rotation; // todo check with LookAt
        // http://wiki.unity3d.com/index.php/SmoothFollow2
    }
}
