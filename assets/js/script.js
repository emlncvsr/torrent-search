document.getElementById("scraper-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const query = document.getElementById("query").value;
    const pages = document.getElementById("pages").value;
    const scraper = document.getElementById("scraper").value;
  
    fetch(`https://api.github.com/repos/emlncvsr/torrent-search/actions/workflows/scrape.yml/dispatches`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.GH_TOKEN}`,
        Accept: "application/vnd.github.v3+json",
      },
      body: JSON.stringify({
        ref: "main",
        inputs: {
          query: query,
          pages: pages,
          scraper: scraper,
        },
      }),
    })
      .then((response) => {
        if (response.status === 204) {
          document.getElementById("results").innerText = "Scrape initiated, check GitHub Actions for progress.";
        } else {
          return response.json().then((data) => {
            document.getElementById("results").innerText = `Error: ${data.message}`;
          });
        }
      })
      .catch((error) => console.error("Error:", error));
  });
  