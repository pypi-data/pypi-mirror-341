# 🦋 ButterRand

ButterRand là một thuật toán sinh số ngẫu nhiên dựa trên hiệu ứng cánh bướm (butterfly effect), sử dụng logistic map và sine map để tạo ra tính hỗn loạn và độ ngẫu nhiên cao.

## Cài đặt

```bash
pip install butterrand

Sử dụng
python
Sao chép
Chỉnh sửa
from butterrand import ButterflyRandom

br = ButterflyRandom(seed="abc123", mode="logistic", noise_function="sin")
print(br.next_float())        # số thực
print(br.next_int(1, 100))    # số nguyên từ 1 đến 99

Tùy chọn
seed: chuỗi hoặc số

mode: "logistic" hoặc "sine"

noise_function: "sin", "cos", "tan", v.v.

epsilon: độ nhiễu nhỏ gây hiệu ứng bướm

yaml
Sao chép
Chỉnh sửa

---

### ✅ 5. `MANIFEST.in`

```text
include README.md