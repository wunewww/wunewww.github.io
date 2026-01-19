# wunewww.github.io  
Personal site for wunewww, serving as the CNAME for [www.uniu.net.cn](https://www.uniu.net.cn)


## Project Overview  
A **Hugo-powered static site** combining personal interests in technology and law. The site functions as a blog to share insights at the intersection of these fields. 
The site is deployed to **GitHub Pages**


## Technology Stack  
| Component               | Details                                  |
|-------------------------|------------------------------------------|
| Static Site Generator   | [Hugo](https://github.com/gohugoio/hugo)                  |
| Theme                   | [Congo](https://github.com/jpanther/congo) |
| Auxiliary Tools         | Python, `uv` (dependency manager), `vale` |


## Setup Instructions  
To run the site locally:  

1. Make sure [Hugo](https://gohugo.io/getting-started/installing/) and Python are installed  
3. Install uv and vale if needed
4. Start Local Server:  
   ```bash
   hugo server -D  # Includes draft content
   hugo server # without drafts
   ```  
   The site will be available at `http://localhost:1313`.

## About the Author  
I always try to explore development, though time is limited. As a law student, I’m more comfortable with paper works and legal analysis—this site bridges my hobbies with my professional focus.  

Welcome to connect!


## License  
See the [LICENSE](LICENSE) file for details.
