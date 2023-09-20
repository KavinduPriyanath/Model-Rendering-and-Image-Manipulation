#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

const unsigned int SCR_WIDTH = 500;
const unsigned int SCR_HEIGHT = 400;

static unsigned int CompileShader(unsigned int type, const char* source) 
{
    unsigned int id = glCreateShader(type); // create shader
    // const char* src = source.c_str(); // get source code
    glShaderSource(id, 1, &source, nullptr); // set source code
    glCompileShader(id); // compile shader

    int result;
    glGetShaderiv(id, GL_COMPILE_STATUS, &result); // get compile status
    if (result == GL_FALSE) // if compile failed
    {
        int length;
        glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length); // get error message length
        char* message = (char*)alloca(length * sizeof(char)); // allocate memory
        glGetShaderInfoLog(id, length, &length, message); // get error message
        std::cout << "Failed to compile " << (type == GL_VERTEX_SHADER ? "vertex" : "fragment") << " shader!" << std::endl; // print error message
        std::cout << message << std::endl; // print error message
        glDeleteShader(id); // delete shader
        return 0;
    }

    return id;
}

static unsigned int CreateShader(const char* vertexShader, const char* fragmentShader)
{
    unsigned int program = glCreateProgram(); // create program
    unsigned int vs = CompileShader(GL_VERTEX_SHADER, vertexShader); // compile vertex shader
    unsigned int fs = CompileShader(GL_FRAGMENT_SHADER, fragmentShader); // compile fragment shader

    glAttachShader(program, vs); // attach vertex shader
    glAttachShader(program, fs); // attach fragment shader
    glLinkProgram(program); // link program
    glValidateProgram(program); // validate program

    glDeleteShader(vs); // delete vertex shader
    glDeleteShader(fs); // delete fragment shader



    return program;
}

float mapX(float x) {
    return (x / SCR_WIDTH) * 2 - 1;
}

float mapY(float y) {
    return (y / SCR_HEIGHT) * 2 - 1;
}

float* MapCoordinates(float x1, float y1, int x2, int y2) {
    float* coordinates = new float[4];
    coordinates[0] = mapX(x1);
    coordinates[1] = mapY(y1);
    coordinates[2] = mapX(x2);
    coordinates[3] = mapY(y2);
    return coordinates;
}

// Vertex shader source code
const char* vertexShaderSource = R"(
    #version 330 core
    layout (location = 0) in vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
)";

// Fragment shader source code
const char* fragmentShaderSource = R"(
    #version 330 core
    out vec4 FragColor;
    void main()
    {
        FragColor = vec4(1.0, 1.0, 0.5, 1.0); // Red color
    }
)";

int main() {
    // Initialize GLFW
    if (!glfwInit()) {
        std::cerr << "GLFW initialization failed." << std::endl;
        return -1;
    }

    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    #ifdef __APPLE__
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    #endif

    // Create a GLFW window
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH,SCR_HEIGHT, "Line drawn from (180,15) to (10,145) in 500X400 window", nullptr, nullptr);
    if (!window) {
        std::cerr << "Failed to create GLFW window." << std::endl;
        glfwTerminate();
        return -1;
    }

    // Make the window's context current
    glfwMakeContextCurrent(window);

    // Load OpenGL function pointers
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Failed to initialize GLAD." << std::endl;
        return -1;
    }
    
    unsigned int shaderProgram = CreateShader(vertexShaderSource, fragmentShaderSource);

    // Set up vertex data
    float vertices[] = {
        -0.9f,  -0.9f,
        0.9f, 0.9f,
    };

    float* coordinates = MapCoordinates(180, 15, 10, 145);

    vertices[0] = coordinates[0];
    vertices[1] = coordinates[1];
    vertices[2] = coordinates[2];
    vertices[3] = coordinates[3];

    // Set up vertex buffer object, vertex array object, and vertex attributes
    unsigned int VBO, VAO;
    glGenBuffers(1, &VBO);
    glGenVertexArrays(1, &VAO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    // Rendering loop
    while (!glfwWindowShouldClose(window)) {
        // Poll for and process events
        glfwPollEvents();

        // Clear the screen
        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Use the shader program
        glUseProgram(shaderProgram);

        // Draw the line segment
        glBindVertexArray(VAO);
        glDrawArrays(GL_LINES, 0, 2);
        glBindVertexArray(0);

        // Swap buffers
        glfwSwapBuffers(window);
    }

    // Clean up
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteProgram(shaderProgram);
    // glDeleteShader(fragmentShader);

    glfwTerminate();
    return 0;
}
