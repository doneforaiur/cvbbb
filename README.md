## CVBBB

**CV** **B**uilder **b**ut **B**etter

GPT meets LaTeX. Type what you did over the years and CVBBB will generate a nice looking CV for you.

## How to use?
- Run `docker run -d -e MODEL_TYPE=falcon -e OPENAI_API_KEY=YOUR_TOKEN -p 5000:5000 ghcr.io/doneforaiur/cvbbb:main`.
- Open `localhost:5000` in your browser.
- Type your CV in the text area as plain text.
- Click on the `Generate CV` button.
- Preview the generated CV.
- Download the generated CV.

**Important note**: If you want to use `falcon` on your GPU, you need to install `nvidia-docker2` and add `--gpus all` flag to the `docker run` command mentioned above.

## Parameters
- `MODEL_TYPE`: The model to use for generating the CV. Avaliable options are `falcon` and `openai`.
- `OPENAI_API_KEY`: Your OpenAI API key if `MODEL_TYPE` is `openai`.



## TODOs

- [ ] Initial development.
- [ ] Add a way to preview the generated CV without downloading it.
- [ ] Add a way to let the user to make adjustments on the generated CV.
- [ ] Add more CV templates.

