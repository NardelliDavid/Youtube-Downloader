import tkinter as tk
from tkinter import messagebox, ttk
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import threading

# Crear la ventana de la app
root = tk.Tk()
root.title("Youtube Downloader")
root.resizable(False, False)

# Función para descargar el video de YouTube en un hilo separado
def descargar_en_hilo():
    # Obtiene la URL ingresada
    url = URLinput.get()
    # Verifica si la URL está vacía
    if not url:
        messagebox.showerror("Error", "El campo URL está vacío.")
        return
    
    try:
        # Deshabilita el input, el boton y la lista
        boton.config(state='disabled')
        lista_descargas.config(state='disabled')
        URLinput.config(state='disabled')
        vaciar_boton.config(state="disabled")
        
        yt = YouTube(url)
        # Obtiene la forma en la que queremos descargar el video
        tipo_descarga_seleccionada = lista_descargas.get()
        
        # Indicamos la ruta a la carpeta descargas
        descargas_ruta = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        # Verifica qué opción seleccionó el usuario
        if tipo_descarga_seleccionada == "Solo video":
            stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first() # Solo video
            filename = "VSI_"+stream.default_filename # Nombre que tendrá el archivo
            stream.download(output_path=descargas_ruta, filename=filename)
            messagebox.showinfo("Informacion", f"Se descargó: {tipo_descarga_seleccionada}\nArchivo: {filename}")
        elif tipo_descarga_seleccionada == "Solo audio":
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first() # Solo audio
            filename = "SA_"+stream.default_filename # Nombre que tendrá el archivo
            stream.download(output_path=descargas_ruta, filename=filename)
            messagebox.showinfo("Informacion", f"Se descargó: {tipo_descarga_seleccionada}\nArchivo: {filename}")
        elif tipo_descarga_seleccionada == "Video y Audio (Basico)":
            stream = yt.streams.get_highest_resolution() # Video y audio
            filename = "VAS_"+stream.default_filename # Nombre que tendrá el archivo
            stream.download(output_path=descargas_ruta, filename=filename)
            messagebox.showinfo("Informacion", f"Se descargó: {tipo_descarga_seleccionada}\nArchivo: {filename}")
        elif tipo_descarga_seleccionada == "Video y Audio (Calidad)":
            video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

            # Obtiene el nombre del audio y el video
            video_filename = 'Video_'+video_stream.default_filename
            audio_filename = 'Audio_'+audio_stream.default_filename
            
            # Descarga el audio y video en la ruta seleccionada y con un nuevo nombre
            video_stream.download(output_path=descargas_ruta, filename=video_filename)
            audio_stream.download(output_path=descargas_ruta, filename=audio_filename)
            
            # Ruta donde están descargados audio y video
            video_ruta = os.path.join(descargas_ruta, video_filename)
            audio_ruta = os.path.join(descargas_ruta, audio_filename)

            try:
                # Carga el video y el audio usando moviepy
                video_clip = VideoFileClip(video_ruta)
                audio_clip = AudioFileClip(audio_ruta)

                # Fusiona el audio y video en uno solo
                final_clip = video_clip.set_audio(audio_clip)

                # Nombre del archivo fusionado
                name_final_video = 'VAC_' + video_stream.default_filename

                # Guarda el video fusionado en descargas
                final_clip.write_videofile(os.path.join(descargas_ruta, name_final_video))

                # Liberar los recursos
                video_clip.close()
                audio_clip.close()

                # Elimina los archivos de audio y video después de fusionarlos
                os.remove(video_ruta)
                os.remove(audio_ruta)

                messagebox.showinfo("Información", f"Se descargó: {tipo_descarga_seleccionada}\nArchivo: {name_final_video}")

            except Exception as merge_error:
                messagebox.showerror("Error", f"Error durante la fusión del video: {str(merge_error)}")

        else:
            messagebox.showerror("Error", "Error: Opción de descarga no válida.")
            return
        
    except Exception as download_error:
        messagebox.showerror("Error", f"Error durante la descarga: {str(download_error)}")
    
    finally:
        # Habilita el input, el boton y la lista después de descargar o mostrar el error
        URLinput.config(state='normal')
        boton.config(state='normal')
        lista_descargas.config(state='readonly')
        vaciar_boton.config(state="normal")

# Función para manejar la descarga en un hilo separado
def obtenerURL():
    threading.Thread(target=descargar_en_hilo).start()

# Funcion del boton de borrar el contenido que esta en la URL
def vaciarURL():
    URLinput.delete(0, tk.END)
    
# Texto indicando que el usuario debe ingresar la URL
URLtext = tk.Label(root, text="Ingrese la URL: ")
URLtext.config(font=('Arial',12))
URLtext.grid(row=0, column=0, padx=10, pady=0)

# input para ingresar la URL
URLinput = tk.Entry(root)
URLinput.configure(bd=1, relief="solid", font=('Arial',10), width=40)
URLinput.grid(row=0, column=1, padx=20, pady=15)

# Lista para seleccionar el tipo de descarga
tipos_de_descarga = ["Video y Audio (Calidad)", "Video y Audio (Basico)", "Solo video", "Solo audio"]
lista_descargas = ttk.Combobox(root, values=tipos_de_descarga, state="readonly", width=20, font=('Arial',15))
lista_descargas.current(0)
lista_descargas.grid(row=1, columnspan=2, pady=10, padx=10)

# Marco para los botones
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2)

# Botón para vaciar el input
vaciar_boton = tk.Button(button_frame, text="Borrar URL", command=vaciarURL)
vaciar_boton.config(bg="#FFC900", bd=1, relief="solid", font=('Arial', 15), fg="black", cursor='hand2')
vaciar_boton.grid(row=0, column=0, padx=10, pady=15)

# Botón que ejecuta la función y descarga el video
boton = tk.Button(button_frame, text="Descargar video", command=obtenerURL)
boton.config(bg="#DF2900", bd=1, relief="solid", font=('Arial', 15), fg="black", cursor='hand2')
boton.grid(row=0, column=1, padx=10, pady=15)

# Centrar el contenido horizontalmente en la ventana
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Ejecutar la aplicación
root.mainloop()
