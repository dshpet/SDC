using UnityEngine;

public class OffsetMovement : MonoBehaviour
{
    public  GameObject PositionProvider;
    private float      m_OffsetX;
    private float      m_OffsetY;
    private float      m_OffsetZ;

    void Start()
    {
        m_OffsetX = this.transform.position.x - PositionProvider.transform.position.x;
        m_OffsetY = this.transform.position.y - PositionProvider.transform.position.y;
        m_OffsetZ = this.transform.position.z - PositionProvider.transform.position.z;
    }
	
	void Update()
    {
        this.transform.position = PositionProvider.transform.position + new Vector3(0, 2, 0); // rotation works incorrectly when applied with X and Z coords
        this.transform.rotation = PositionProvider.transform.rotation; // todo check with LookAt
        // http://wiki.unity3d.com/index.php/SmoothFollow2
    }
}
