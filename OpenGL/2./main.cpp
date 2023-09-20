#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

const unsigned int SCR_WIDTH = 500;
const unsigned int SCR_HEIGHT = 400;

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
        FragColor = vec4(1.0, 0.0, 0.0, 1.0); // Red color
    }
)";

float mapX(int x) {
    return ((float)x / SCR_WIDTH) * 2 - 1;
}

float mapY(int y) {
    return ((float)y / SCR_HEIGHT) * 2 - 1;
}

float* bresenham(int xStart, int yStart, int xEnd, int yEnd)
{
    int dx = xEnd - xStart;
    int dy = yEnd - yStart;
    float* points = new float[2 * (xEnd - xStart) + 2];

    int m = 2 * dy;
    int e = m - dx;
    
    for (int x=xStart, y=yStart, i=0; x<=xEnd; x++) {
        points[i++] = mapX(x);
        points[i++] = mapY(y);

        if (e >= 0) {
            y++;
            e += m - 2 * dx;
        } else {
            e += m;
        }
    }

    return points;
}


int main() {
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

    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Bresenham Line for line connecting (10,5) and (50,50)", nullptr, nullptr);
    if (!window) {
        std::cerr << "Failed to create GLFW window." << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Failed to initialize GLAD." << std::endl;
        return -1;
    }

    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
    glCompileShader(vertexShader);

    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, nullptr);
    glCompileShader(fragmentShader);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    int xStart = 100 , yStart = 5;
    int xEnd = 300, yEnd = 200;

    int pointsCount = xEnd - xStart + 1;

    float* points = bresenham(xStart, yStart, xEnd, yEnd);

    // Create Vertex Array Object (VAO)
    unsigned int VAO;
    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);

    // Create Vertex Buffer Object (VBO)
    unsigned int VBO;
    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);

    glBufferData(GL_ARRAY_BUFFER, sizeof(float) * 2 * pointsCount , points, GL_STATIC_DRAW);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    // Rendering loop
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // glPointSize(5.0f);

        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);

        // Draw the line segment
        glDrawArrays(GL_POINT, 0, pointsCount);

        glBindVertexArray(0);
        glfwSwapBuffers(window);
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}
