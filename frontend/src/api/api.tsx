export default class API {
  /** Singleton instance of the API class. */
  static api: null | API;
  api = null;

  URL = "http://localhost:8000/api";

  fileURL = () => `${this.URL}/file`;

  static getAPI() {
    if (this.api == null) {
      this.api = new API();
    }
    return this.api;
  }

  fetchAdvanced(url: string, init: RequestInit) {
    // Default initialization if not provided
    // If no init parameter is used, create empty init
    if (typeof init === "undefined") {
      init = {
        headers: {},
      };
    }
    // If no headers parameter is used, create empty header
    if (typeof init.headers === "undefined") {
      init["headers"] = {};
    }

    return fetch(url, init).then((res) => {
      // The Promise returned from fetch() won’t reject on HTTP error status even if the response is an HTTP 404 or 500.
      if (!res.ok) {
        throw Error(`${res.status} ${res.statusText}`);
      }
      try {
        return res.json();
      } catch (err) {
        console.error("Error parsing JSON", err);
        return [];
      }
    });
  }

  postConversation(pdfFile: FormData) {
    // const reader = new FileReader();
    // reader.readAsDataURL(audioFile);
    // reader.onloadend = async () => {
    // const base64String = reader.result?.split(",")[1];
    // };

    const url = this.fileURL();
    console.log(pdfFile);
    try {
      return this.fetchAdvanced(url, {
        method: "POST",
        body: pdfFile,
      });
    } catch {
      console.error("Error posting conversation");
      return [];
    }
  }
}
