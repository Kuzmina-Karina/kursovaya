#include <vector>
#include <string>
#include <algorithm>

extern "C" {
    // Функция для поиска строк в таблице (возвращает индексы строк)
    void find_matches(const char** data, int rows, int cols, const char* query, int* results) {
        std::string query_str(query);
        for (int i = 0; i < rows; ++i) {
            results[i] = 0;  // 0 = не найдено, 1 = найдено
            for (int j = 0; j < cols; ++j) {
                std::string cell(data[i * cols + j]);
                if (cell.find(query_str) != std::string::npos) {
                    results[i] = 1;
                    break;
                }
            }
        }
    }
}