using UnityEngine;

public class ScreenshotMaker : MonoBehaviour
{
    //
    // Config
    //

    public string ScreenshotsFolder = "Screenshots";
    public int    Scale             = 1;

    //
    // Members
    //

    private int m_ScreenshotsTaken = 0;

    //
    // Functions
    //

	void Update()
    {
		if (Input.GetKeyUp(KeyCode.F1))
        {
            string ScreenshotsPath = Application.dataPath + "/../" + ScreenshotsFolder;
            if (!System.IO.Directory.Exists(ScreenshotsPath))
                System.IO.Directory.CreateDirectory(ScreenshotsPath);

            string TimeNow = System.DateTime.Now.ToString("yyyyMMddHHmmssFFF");
            string Path    = ScreenshotsPath + "/" + TimeNow + ".png";

            ScreenCapture.CaptureScreenshot(Path, Scale);

            m_ScreenshotsTaken++;
        }
	}
}
