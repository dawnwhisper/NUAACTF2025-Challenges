#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// 解码 URL 编码的字符串
void urldecode(char *dst, const char *src) {
    char a, b;
    while (*src) {
        if ((*src == '%') && ((a = src[1]) && (b = src[2])) && 
            (isxdigit(a) && isxdigit(b))) {
            if (a >= 'a') a -= 'a' - 'A';
            if (a >= 'A') a -= ('A' - 10);
            else a -= '0';
            if (b >= 'a') b -= 'a' - 'A';
            if (b >= 'A') b -= ('A' - 10);
            else b -= '0';
            *dst++ = 16 * a + b;
            src += 3;
        } else if (*src == '+') {
            *dst++ = ' '; // '+' 转换为空格
            src++;
        } else {
            *dst++ = *src++;
        }
    }
    *dst = '\0';
}

int main() {
    // 输出完整的 HTTP 响应头
    printf("HTTP/1.1 200 OK\r\n");
    printf("Content-Type: text/html; charset=utf-8\r\n\r\n");
    
    char *encoded_expr = getenv("expr");
    if (encoded_expr == NULL || encoded_expr[0] == '\0') {
        printf("<html><body><h1>错误: 未指定计算表达式</h1></body></html>");
        return 1;
    }
    
    // 解码 URL 编码的表达式
    char expr[512];
    urldecode(expr, encoded_expr);
    
    // 使用 bc 计算表达式
    char command[512];
    snprintf(command, sizeof(command), "echo '%s' | bc", expr);
    
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        printf("<html><body><h1>错误: 无法计算表达式</h1></body></html>");
        return 1;
    }
    
    // 读取计算结果
    char result[128] = {0};
    fgets(result, sizeof(result), fp);
    pclose(fp);
    
    // 移除结果中的换行符
    result[strcspn(result, "\n")] = '\0';
    
    // 输出结果页面
    printf("<html><body>"); 
    printf("<h1>计算结果</h1>");
    printf("<p>表达式: %s</p>", expr);
    printf("<p>结果: %s</p>", result);
    printf("<a href='/index.html'>返回首页</a>");
    printf("</body></html>");
    
    return 0;
}