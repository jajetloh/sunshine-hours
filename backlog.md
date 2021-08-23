# Current tasks

- **Add a colour scale which utilises the CIELAB scale?** Particularly as the task mentions the choice of colour specifically. Explanation of CIELAB [here](https://www.vis4.net/blog/2011/12/avoid-equidistant-hsv-colors/), google for more. [``python-colormath``](https://python-colormath.readthedocs.io/en/latest/) is a possible library to use for this.
- Add more charts/layers to the app
- Incorporate daylight hours somehow? The calculation is in ``solar_elevation`` in ``sunshine-notebook.ipynb``
- Find more data to add to the dataset

# Reminders
## Initial setup

Assuming ``virtualenv`` is already installed globally, and repository has been cloned. Ensure current active directory is the root folder of the repository.

```bash
virtualenv sunshine-env
source sunshine-env/bin/activate
pip install ipykernel
ipython kernel install --user --name=sunshine-kernel
```

May need to restart VSCode (if using VSCode instead of broswer to run notebooks)
```bash
pip install -r requirements.txt
```
## How to run app locally
Activate virtual environment with <br>
``source sunshine-env/bin/activate`` <br>
Then run app with <br>
``streamlit run main-app.py``

## Saving/installing current pip dependencies
``pip freeze requirements.txt`` <br>
``pip install -r requirements.txt``


# Useful links
- [Streamlit Documentation](https://docs.streamlit.io/en/stable/api.html)
- [Deploying Streamlit on share.streamlit.io](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html#log-in-to-share-streamlit-io)
- [pydeck Layers](https://deckgl.readthedocs.io/en/latest/index.html)