# wunewww.github.io  
Personal site for wunewww, serving as the CNAME for [www.uniu.net.cn](https://www.uniu.net.cn)


## Project Overview  
A **Hugo-powered static site** combining personal interests in technology and law. The site functions as a blog to share insights at the intersection of these fields.


## Technology Stack  
| Component               | Details                                  |
|-------------------------|------------------------------------------|
| Static Site Generator   | [Hugo](https://github.com/gohugoio/hugo)                  |
| Theme                   | [Congo](https://github.com/jpanther/congo) |
| Auxiliary Tools         | Python, `uv` (dependency manager), `vale` |


## Setup Instructions  
To run the site locally:  

1. **Install Hugo**:  
   Follow the [official Hugo installation guide](https://gohugo.io/getting-started/installing/) (ensure you install the **extended version** for Tailwind CSS support).  

2. **Install Python**:  
   Use the version specified in `.python-version` (via `pyenv` or direct download).  

3. **Install Python Dependencies**:  
   Run `uv sync` (or `pip install -r requirements.txt` if using pip).  

4. **Start Local Server**:  
   ```bash
   hugo server -D  # Includes draft content
   hugo server # without drafts
   ```  
   The site will be available at `http://localhost:1313`.


## Deployment  
The site is deployed to **GitHub Pages**:  
- Use Hugo's built-in deployment: `hugo deploy` (configure via `config.toml`).  
- CNAME is set for `www.uniu.net.cn` (configured in `static/CNAME`).


## About the Author  
I always try to explore development, though time is limited. As a law student, I’m more comfortable with paper works and legal analysis—this site bridges my hobbies with my professional focus.  

Welcome to connect!


## License  
See the [LICENSE](LICENSE) file for details.
