import PySimpleGUI as sg
import pyodbc
import nhaplieu


def main():
    # Function to check credentials against the database
    def verify_credentials(tendangnhap, matkhau):
        # Establish the connection
        cnx = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
                            SERVER=Thuan-Nguyen; \
                            Database=sql; UID=hoa; PWD=123;')
        cursor = cnx.cursor()

        # Query to check if the username and password exist
        cursor.execute('SELECT * FROM Data1 WHERE username = ? AND password = ?',
                       (tendangnhap, matkhau))
        data = cursor.fetchone()

        # Close the connection
        cursor.close()
        cnx.close()

        return data is not None

    # Đường dẫn đến file icon
    icon_path = 'icon.ico'  # Đổi thành đường dẫn và tên file icon thực tế trên máy của bạn

    # Thiết lập icon cho cửa sổ chương trình
    sg.set_options(icon=icon_path)

    # Define the layout
    layout = [
        [sg.Text("Tên Đăng Nhập")],
        [sg.Input(key='tendangnhap')],
        [sg.Text("Mật Khẩu")],
        [sg.Input(key='matkhau', password_char='*')],  # Ẩn mật khẩu bằng *
        [sg.Button("Đăng Nhập"), sg.Button("Exit")],
        [sg.Text("", key="tinnhan")]
    ]

    # Create the window
    window = sg.Window("Đăng nhập tài khoản", layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Exit":
            # Ask for confirmation before exiting
            if sg.popup_yes_no('Bạn có muốn thoát không?', 'Thoát chương trình') == 'Yes':
                break
        elif event == "Đăng Nhập":
            dktendangnhap = values["tendangnhap"]
            dkmatkhau = values["matkhau"]

            if verify_credentials(dktendangnhap, dkmatkhau):
                window["tinnhan"].update("Đăng Nhập Thành Công")
                window.hide()  # Ẩn màn hình đăng nhập

                # Chuyển sang màn hình nhaplieu
                nhaplieu.main()

                window.un_hide()  # Hiện lại màn hình đăng nhập sau khi nhaplieu đóng

            else:
                window["tinnhan"].update("Đăng Nhập Không Đúng, Mật Khẩu và/hoặc Tên Đăng Nhập Không Đúng")
    # Close the window
    window.close()

if __name__ == "__main__":
    main()
