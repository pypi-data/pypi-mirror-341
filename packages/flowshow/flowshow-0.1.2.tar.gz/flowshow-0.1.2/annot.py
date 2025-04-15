import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from mohtml import p, tailwind_css, div, br, pre

    stream = (i for i in "abcdefghijk")
    get_annot, set_annot = mo.state([])
    get_stream, set_stream = mo.state(next(stream))

    tailwind_css()
    return (
        br,
        div,
        get_annot,
        get_stream,
        mo,
        p,
        pre,
        set_annot,
        set_stream,
        stream,
        tailwind_css,
    )


@app.cell
def _(get_stream, mo, set_annot, set_stream, stream):
    def update(value):
        set_annot(lambda d: d + [{"annot": value, "text": get_stream()}])
        set_stream(lambda d: next(stream))

    buttons = mo.ui.array([
        mo.ui.button(label="yes", on_change=lambda d: update("yes"), keyboard_shortcut="Ctrl-u"),
        mo.ui.button(label="no", on_change=lambda d: update("no"), keyboard_shortcut="Ctrl-i"),
        mo.ui.button(label="maybe", on_change=lambda d: update("maybe"), keyboard_shortcut="Ctrl-o"),
        mo.ui.button(label="skip", on_change=lambda d: update("skip"), keyboard_shortcut="Ctrl-p"),
    ])
    return buttons, update


@app.cell
def _(br, buttons, div, get_stream, mo, p, pre):
    mo.vstack([
        div(
            p("Does this text suggest that the abstract indicates a new dataset?"),
            br(),
            pre(
                get_stream(),
                klass="bg-gray-100 p-2 rounded-lg"
            ) ,
            br(),
            mo.hstack(buttons),
            klass="bg-gray-200 text-center p-8 rounded-xl",
        ),
    ])
    return


@app.cell
def _(get_annot):
    get_annot()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
