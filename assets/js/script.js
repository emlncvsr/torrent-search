document.getElementById("scraper-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const query = document.getElementById("query").value;
  const pages = document.getElementById("pages").value;
  const scraper = document.getElementById("scraper").value;

  fetch(`http://localhost:5000/scrape`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query,
      pages: pages,
      scraper: scraper,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("results").innerText = data.message;
    })
    .catch((error) => console.error("Error:", error));
});
