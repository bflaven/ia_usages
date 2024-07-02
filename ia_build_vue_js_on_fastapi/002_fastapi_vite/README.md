## 002_fastapi_vite






This repo goes hand-in-hand with the following blog post
- [https://dimmaski.com/serve-vue-fastapi/](https://dimmaski.com/serve-vue-fastapi/)
## Serve Backend locally

```sh


# Conda Environment
conda create --name sentiment_analysis python=3.9.13
conda info --envs
source activate sentiment_analysis
conda deactivate



# go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/002_fastapi_vite/

# LAUNCH THE API
uvicorn api.main:app --reload



```

## Serve Frontend locally
```sh
# go to path
cd /Users/brunoflaven/Documents/01_work/blog_articles/build_vue_js_on_fastapi/002_fastapi_vite/

# create the directory
npm init vite ui



# ls -l
# You should see the ui directory
# go to the directory created
cd ui

# install dependencies
npm install

# start the development server
npm run dev
# check http://localhost:5173/

# build for production
npm run build





```

## Run FE and BE in hot-reload mode
```
npm run watch --prefix ui & uvicorn api/main:app --reload && fg
```
