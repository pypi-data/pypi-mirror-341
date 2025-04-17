from kodosumi.inputs import *

def test_model_build():
    model = Model(
        P("# Hello World"),
        InputText(label="Name", name="name", placeholder="Enter your name"),
        InputNumber(label="Age", name="age"),
        P("Do you feel _active_?"),
        InputCheckbox(label="Active", name="active"),
        P("What is your favorite color?"),
        InputSelect(label="Color", name="color", 
                    options=["Red", "Green", "Blue"]),
        InputDate(label="Birthday", name="birthday"),
        P("Do you know the time of your birth, really?"),
        InputTime(label="Time", name="time"),
        P("Would you like me to get back to you later in the future?"),
        InputCheckbox(label="Get back to me in Future", name="future", default=False),
        Button(label="Submit Form", value="submit"),
        Button(label="Cancel Request", value="cancel")
    )
    print(model)
    html = model.render()
    print(html)
    html = model.get_page()
    open("test.html", "w").write(html)