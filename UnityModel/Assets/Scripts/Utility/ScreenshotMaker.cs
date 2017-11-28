using UnityEngine;
using System;
using System.IO;

/// <summary>
/// Logging for neural network
/// </summary>
public class ScreenshotMaker : MonoBehaviour
{
    //
    // Config
    //

    public string DataFolder = "SavedData";
    public int    Scale      = 1;

    //
    // Members
    //

    private string m_DataPath = "";

    //
    // Functions
    //

    void Start()
    {
        m_DataPath = Application.dataPath + "/../" + DataFolder;
        if (!System.IO.Directory.Exists(m_DataPath))
            System.IO.Directory.CreateDirectory(m_DataPath);        
    }

    void Update()
    {
        string TimeNow = System.DateTime.Now.ToString("yyyyMMddHHmmssFFF");

        string BasePath = m_DataPath + "/" + TimeNow;
		// Capture screenshot
        {
            string PicturePath = BasePath + ".png";
            ScreenCapture.CaptureScreenshot(PicturePath, Scale);
        }
        // Capture input
        {
            string InputString = "";
            foreach (KeyCode kcode in Enum.GetValues(typeof(KeyCode)))
            {
                if (Input.GetKeyDown(kcode))
                    InputString += kcode;
            }

            // maybe should pump an empty file for training sake
            if (InputString != "")
                System.IO.File.WriteAllText(BasePath + ".txt", InputString);
        }
	}
}
